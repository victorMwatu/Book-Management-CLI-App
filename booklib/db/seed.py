from booklib.db.database import SessionLocal, engine
from booklib.db.models import Base, Author, Book, Borrower, BorrowRecords
from datetime import datetime

# Optional: create tables if not already created
Base.metadata.create_all(bind=engine)

def seed_data():
    session = SessionLocal()
    try:
        # Authors
        author1 = Author(name="Isaac Asimov", birth_year=1920, country="Russia")
        author2 = Author(name="Frank Herbert", birth_year=1920, country="USA")
        author3 = Author(name="Malcolm Gladwell", birth_year=1963, country="Canada")
        author4 = Author(name="Leo Tolstoy", birth_year=1828, country="Russia")
        author5 = Author(name="George Orwell", birth_year=1903, country="UK")
        session.add_all([author1, author2, author3, author4, author5])
        session.commit()

        # Books
        book1 = Book(title="Foundation", year=1951, genre="Sci-Fi", author=author1)
        book2 = Book(title="Dune", year=1965, genre="Sci-Fi", author=author2)
        book3 = Book(title="Blink", year=2005, genre="Psychology", author=author3)
        book4 = Book(title="Outliers", year=2008, genre="Non-Fiction", author=author3)
        book5 = Book(title="War and Peace", year=1869, genre="Historical Fiction", author=author4)
        book6 = Book(title="1984", year=1949, genre="Dystopian", author=author5)
        book7 = Book(title="Animal Farm", year=1945, genre="Political Satire", author=author5)
        session.add_all([book1, book2, book3, book4, book5, book6, book7])
        session.commit()

        # Borrowers
        borrower1 = Borrower(name="Carmen Bornero", contacts="+254722000000")
        borrower2 = Borrower(name="Mike", contacts="mike@example.com")
        borrower3 = Borrower(name="Lucille 2ndFloor", contacts="+254733100000")
        session.add_all([borrower1, borrower2, borrower3])
        session.commit()

        # BorrowRecords
        record1 = BorrowRecords(book=book1, borrower=borrower1, borrow_date=datetime.now())
        record2 = BorrowRecords(book=book3, borrower=borrower2, borrow_date=datetime.now())
        record3 = BorrowRecords(book=book5, borrower=borrower3, borrow_date=datetime.now())
        session.add_all([record1, record2, record3])
        session.commit()

        print("Test data added successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error adding seed data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
