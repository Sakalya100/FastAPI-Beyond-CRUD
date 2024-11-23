from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import (
    UserCreateModel,
    UserModel,
    UserBooksModel,
    UserLoginModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from src.db.main import get_session
from .utils import (
    create_access_token,
    decode_token,
    verify_password,
    generate_passwd_hash,
    create_url_safe_token,
    decode_url_safe_token,
)
from src.mail import create_message_new, send_email
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist
from src.errors import InvalidToken, UserAlreadyExists, UserNotFound, InvalidCredentials
from src.mail import mail, create_message
from src.config import Config
from src.celery_tasks import send_mail

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


# @auth_router.post('/send_mail')
# async def send_mail(emails: EmailModel):
#     emails = emails.addresses

#     html = "<h1> Welcome to the Bookly APP </h1>"

#     message = create_message(
#         recipients=emails,
#         subject="Welcome",
#         body=html
#     )

#     await mail.send_message(message)


#     return JSONResponse(
#         content={
#             "message": "Email sent successfully"
#         }
#     )
# @auth_router.post("/send_mail")
# async def send_mails(emails: EmailModel):
#     email = emails.addresses

#     html = "<h1> Welcome to the Bookly APP </h1>"

#     sending_data = create_message_new(subject=html)

#     try:
#         status = send_email(data=sending_data, recipient_email=email)

#         if status:
#             return JSONResponse(content={"message": "Email sent successfully"})
#         else:
#             return JSONResponse(
#                 content={"message": "Ooops Something went wrong. Email not Sent!"}
#             )
#     except Exception as e:
#         return JSONResponse(content={"message": "Email not sent", "error": str(e)})


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_acccount(
    user_data: UserCreateModel, bg_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
        <h1> Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message_new(subject="Verify your email")

    # send_mail.delay(email, message, html_message)
    bg_tasks.add_task(send_email,message, email, html_message)

    return {
        "message": "Account Created! Check email to verify your account.",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Email verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password_hash

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": email, "user_uid": str(user.uid), "role": user.role}
            )

            refresh_token = create_access_token(
                user_data={"email": email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login Successfull!!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/profile", response_model=UserBooksModel)
async def get_current_user_details(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Loggedout successfully!!"}, status_code=status.HTTP_200_OK
    )


"""
1. PROVIDE THE EMAIL -> password reset request
2. SEND PASSWORD RESET LINK
3. RESET PASSWORD -> password reset confirmation
"""


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel, session: AsyncSession = Depends(get_session)):
    email = email_data.email

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise UserNotFound()

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """

    message = create_message_new(subject="Reset Your Password")

    mail_status = send_email(message, recipient_email=email, body=html_message)

    return JSONResponse(
        content={"message": "Please check for instructions to reset your password"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):

    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST)
    
    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"password_hash": generate_passwd_hash(passwords.new_password)}, session)

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during reseting password"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
