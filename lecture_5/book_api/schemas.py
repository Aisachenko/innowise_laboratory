from pydantic import BaseModel
from typing import Optional

# Base schema for Book
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

# Schema for creating a new book
class BookCreate(BookBase):
    pass

# Schema for updating a book
class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

# Schema for Book response (includes ID)
class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode

# Schema for search parameters
class BookSearch(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None