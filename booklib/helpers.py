from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .db.models import Author, Book, Borrower, BorrowRecords
from datetime import datetime
from sqlalchemy.exc import NoResultFound

# Books Management
def add_book(session, title, author, year, genre):
    '''add-book → Add a new book with title, author, year, genre.'''
    if not title or not author:
        raise ValueError("Both title and author are required")

    # Check if author already exists
    db_author = session.query(Author).filter_by(name=author).first()
    if not db_author:
        db_author = Author(name=author)
        session.add(db_author)
        session.commit()

    # Create new book
    book = Book(title=title, year=year, genre=genre, author=db_author)
    session.add(book)
    session.commit()
    session.refresh(book)

    return book

def list_books(session):
    '''list-books → Show all books, with availability status.'''
    pass

def search_book(session, title):
    '''search-book --title "Dune" → Find books by title, author, or genre.'''
    pass

def delete_book(session, id):
    '''delete-book <book_id> → Remove a book.'''
    pass

def update_book(session, id):
    '''update-book <book_id> → Change title/author/year.'''
    pass


# Author Management
def add_author(session, name, birth_year, country):
    '''add-author → Add new author.'''
    pass

def list_authors(session):
    '''list-authors → Show authors and how many books they have.'''
    pass

def find_author(session, name):
    '''find-author --name "Asimov"'''
    pass


# Borrower Management
def add_borrower(session, name, contacts):
    '''add-borrower → Register a new person.'''
    pass

def list_borrowers(session):
    '''list-borrowers → Show who can borrow.'''
    pass

def delete_borrower(session, id):
    '''delete-borrower <id>'''
    pass


# Borrowing / Returning
def borrow(session, book, borrower):
    '''borrow <book_id> --by <borrower_id>'''
    pass

def check_availability(session, book):
    '''Checks if book is available.'''
    pass

def mark_as_unavailable(session, book):
    '''Marks book as unavailable.'''
    pass

def create_borrow_record(session, book, borrower):
    '''Creates BorrowRecord with borrow_date=NOW().'''
    pass

def return_book(session, book, borrower):
    '''return <book_id>'''
    pass

def update_return_date(session, book_record):
    '''Updates return_date.'''
    pass

def mark_as_available(session, book):
    '''Marks book available again.'''
    pass


# Reports / Queries
def get_borrowed_books(session, borrow_records):
    '''borrowed-books → List all currently borrowed books with borrower names.'''
    pass

def borrowing_history(session, book):
    '''history <book_id> → Show all past borrowing records for a book.'''
    pass

def late_returns(session, borrow_records):
    '''late-returns --days 30 → Find overdue books.'''
    pass

def top_authors(session, number):
    '''top-authors → List authors by number of books in library.'''
    pass

def top_borrower(session, number):
    '''top-borrowers → People who borrowed the most.'''
    pass
