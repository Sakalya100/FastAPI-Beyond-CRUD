from pydantic import BaseModel
import uuid
from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel
from typing import Optional, List
from datetime import datetime

class Book(BaseModel):
    uid: uuid.UUID
    user_uid: Optional[uuid.UUID] = None # This will throw an error when calling the get_all_books endpoint because the response model is Book and we always expect
                        # a user_uid. But for some books we have user_uid as None. 
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    
class BookDetailModel(Book):
    reviews: List[ReviewModel]
    tags: List[TagModel]
    
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str