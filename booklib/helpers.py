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

    db_author = session.query(Author).filter_by(name=author).first()
    if not db_author:
        db_author = Author(name=author)
        session.add(db_author)
        session.commit()

    book = Book(title=title, year=year, genre=genre, author=db_author, available=True)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def list_books(session):
    '''list-books → Show all books, with availability status.'''
    return session.query(Book).all()

def search_book(session, title):
    '''search-book --title "Dune" → Find books by title, author, or genre.'''
    return session.query(Book).join(Author).filter(
        (Book.title.ilike(f"%{title}%")) |
        (Book.genre.ilike(f"%{title}%")) |
        (Author.name.ilike(f"%{title}%"))
    ).all()

def delete_book(session, id):
    '''delete-book <book_id> → Remove a book.'''
    book = session.query(Book).get(id)
    if not book:
        raise NoResultFound("Book not found")
    session.delete(book)
    session.commit()
    return True

def update_book(session, id, title=None, author=None, year=None, genre=None):
    '''update-book <book_id> → Change title/author/year.'''
    book = session.query(Book).get(id)
    if not book:
        raise NoResultFound("Book not found")
    if title:
        book.title = title
    if author:
        db_author = session.query(Author).filter_by(name=author).first()
        if not db_author:
            db_author = Author(name=author)
            session.add(db_author)
            session.commit()
        book.author = db_author
    if year:
        book.year = year
    if genre:
        book.genre = genre
    session.commit()
    return book


# Author Management
def add_author(session, name, birth_year, country):
    '''add-author → Add new author.'''
    author = Author(name=name, birth_year=birth_year, country=country)
    session.add(author)
    session.commit()
    return author

def list_authors(session):
    '''list-authors → Show authors and how many books they have.'''
    return session.query(Author, func.count(Book.id)).join(Book, isouter=True).group_by(Author.id).all()

def find_author(session, name):
    '''find-author --name "Asimov"'''
    return session.query(Author).filter(Author.name.ilike(f"%{name}%")).all()


# Borrower Management
def add_borrower(session, name, contacts):
    '''add-borrower → Register a new person.'''
    borrower = Borrower(name=name, contacts=contacts)
    session.add(borrower)
    session.commit()
    return borrower

def list_borrowers(session):
    '''list-borrowers → Show who can borrow.'''
    return session.query(Borrower).all()

def delete_borrower(session, id):
    '''delete-borrower <id>'''
    borrower = session.query(Borrower).get(id)
    if not borrower:
        raise NoResultFound("Borrower not found")
    session.delete(borrower)
    session.commit()
    return True


# Borrowing / Returning
def borrow(session, book_title, borrower_name):
    """Borrow a book by title for a borrower by name."""

    borrower = session.query(Borrower).filter_by(name=borrower_name).first()
    if not borrower:
        borrower = Borrower(name=borrower_name)
        session.add(borrower)

    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        raise NoResultFound(f"Book '{book_title}' not found")

    if not check_availability(session, book):
        raise ValueError(f"'{book.title}' is not available")

    mark_as_unavailable(session, book)
    record = create_borrow_record(session, book, borrower)
    session.commit()
    return record

def check_availability(session, book):
    '''Checks if book is available.'''
    return book.available

def mark_as_unavailable(session, book):
    '''Marks book as unavailable.'''
    book.available = False
    session.commit()

def create_borrow_record(session, book, borrower):
    '''Creates BorrowRecord with borrow_date=NOW().'''
    record = BorrowRecords(book_id=book.id, borrower_id=borrower.id, borrow_date=datetime.now(), returned=False)
    session.add(record)
    session.commit()
    return record

def return_book(session, book_title, borrower_name):
    '''return <book_id>'''

    borrower = session.query(Borrower).filter_by(name=borrower_name).first()
    if not borrower:
        raise NoResultFound(f"Borrower '{borrower_name}' not found")

    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        raise NoResultFound(f"Book '{book_title}' not found")

    record = session.query(BorrowRecords).filter_by(book_id=book.id, borrower_id=borrower.id, returned=False).first()
    if not record:
        raise NoResultFound("Active borrow record not found")
    update_return_date(session, record)
    mark_as_available(session, book)
    return record

def update_return_date(session, book_record):
    '''Updates return_date.'''
    book_record.return_date = datetime.now()
    book_record.returned = True
    session.commit()

def mark_as_available(session, book):
    '''Marks book available again.'''
    book.available = True
    session.commit()


# Reports / Queries
def get_borrowed_books(session, borrow_records=None):
    '''borrowed-books → List all currently borrowed books with borrower names.'''
    q = session.query(BorrowRecords).filter_by(returned=False).all()
    return q

def borrowing_history(session, book):
    '''history <book_id> → Show all past borrowing records for a book.'''
    return session.query(BorrowRecords).filter_by(book_id=book.id).all()

def late_returns(session, borrow_records=None, days=30):
    '''late-returns --days 30 → Find overdue books.'''
    cutoff = datetime.now() - timedelta(days=days)
    return session.query(BorrowRecords).filter(BorrowRecords.returned == False, BorrowRecords.borrow_date < cutoff).all()

def top_authors(session, number=5):
    '''top-authors → List authors by number of books in library.'''
    return session.query(Author, func.count(Book.id).label("book_count")).join(Book).group_by(Author.id).order_by(func.count(Book.id).desc()).limit(number).all()

def top_borrower(session, number=5):
    '''top-borrowers → People who borrowed the most.'''
    return session.query(Borrower, func.count(BorrowRecords.id).label("borrow_count")).join(BorrowRecords).group_by(Borrower.id).order_by(func.count(BorrowRecords.id).desc()).limit(number).all()
