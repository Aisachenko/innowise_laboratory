from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

# Import from local modules
from database import engine, get_db
from models import Book, Base
from schemas import BookCreate, BookResponse, BookUpdate, BookSearch

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Collection API",
    description="A simple API to manage your book collection",
    version="1.0.0"
)

# Home endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Book Collection API"}

# 1. POST /books/ - Add a new book
@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the collection
    """
    # Check if book already exists
    existing_book = db.query(Book).filter(
        Book.title == book.title,
        Book.author == book.author
    ).first()
    
    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="Book with this title and author already exists"
        )
    
    # Create new book instance
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# 2. GET /books/ - Get all books (with optional pagination)
@app.get("/books/", response_model=List[BookResponse])
def get_all_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all books from the collection with pagination
    """
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

# 3. DELETE /books/{book_id} - Delete a book by ID
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by its ID
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return None

# 4. PUT /books/{book_id} - Update book details
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update book details by ID
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update only provided fields
    update_data = book_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

# 5. GET /books/search/ - Search books by title, author, or year
@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Search books by title, author, or year
    """
    query = db.query(Book)
    
    # Build search conditions
    conditions = []
    if title:
        conditions.append(Book.title.ilike(f"%{title}%"))
    if author:
        conditions.append(Book.author.ilike(f"%{author}%"))
    if year:
        conditions.append(Book.year == year)
    
    # Apply conditions if any
    if conditions:
        query = query.filter(or_(*conditions))
    
    books = query.all()
    return books

# 6. GET /books/{book_id} - Get a specific book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Get a specific book by its ID
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)