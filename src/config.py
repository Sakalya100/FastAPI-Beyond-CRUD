from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str 
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int=6379
    REDIS_PASSWORD: str
    REDIS_URL: str = "redis://default:rZ1wRUEAtZdiehxKvYpV2avbDzGVFm8f@redis-16405.c305.ap-south-1-1.ec2.redns.redis-cloud.com:16405"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup=True