import click
from sqlalchemy.exc import SQLAlchemyError
from booklib.db.database import SessionLocal
from booklib import helpers

logo = '''
██████   ██████   ██████  ██   ██ ██      ██ ██ ██████  
██   ██ ██    ██ ██    ██ ██  ██  ██      ██ ██ ██   ██ 
██████  ██    ██ ██    ██ █████   ██      ██ ██ ██████  
██   ██ ██    ██ ██    ██ ██  ██  ██      ██ ██ ██   ██ 
██████   ██████   ██████  ██   ██ ███████ ██ ██ ██████  
                                                        
                    BOOKLIB CLI
'''

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """BookLib CLI – manage your books and borrowers."""
    click.echo(logo)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Click commands to be used when arguments passed

@cli.command("add-book")
@click.option("--title", prompt="Book title")
@click.option("--author", prompt="Author name")
@click.option("--year", type=int, prompt="Year", required=False)
@click.option("--genre", prompt="Genre", required=False)
def add_book_command(title, author, year, genre):
    """Add a new book."""
    try:
        with SessionLocal() as session:
            helpers.add_book(session, title, author, year, genre)
            session.commit()
            click.echo(f"Book '{title}' by {author} added.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("list-books")
def list_books_command():
    """List all books."""
    try:
        with SessionLocal() as session:
            books = helpers.list_books(session)
            if not books:
                click.echo("No books found.")
            else:
                for book in books:
                    click.echo(f"{book.id}: {book.title} by {book.author.name}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("search-book")
@click.argument("query")
def search_book_command(query):
    """Search books by title, author, or genre."""
    with SessionLocal() as session:
        results = helpers.search_book(session, query)
        for b in results:
            click.echo(f"{b.id}: {b.title} by {b.author.name}")


@cli.command("delete-book")
@click.argument("book_id", type=int)
def delete_book_command(book_id):
    """Delete a book by ID."""
    with SessionLocal() as session:
        helpers.delete_book(session, book_id)
        session.commit()
        click.echo("Book deleted.")


@cli.command("update-book")
@click.argument("book_id", type=int)
def update_book_command(book_id):
    """Update a book by ID (interactive prompts)."""
    with SessionLocal() as session:
        helpers.update_book(session, book_id)
        session.commit()
        click.echo("Book updated.")


# Authors commands
@cli.command("add-author")
@click.argument("name")
@click.option("--birth", type=int, required=False)
@click.option("--country", required=False)
def add_author_command(name, birth, country):
    """Add an author"""
    with SessionLocal() as session:
        helpers.add_author(session, name, birth, country)
        session.commit()
        click.echo(f"Author '{name}' added.")


@cli.command("list-authors")
def list_authors_command():
    """List authors"""
    with SessionLocal() as session:
        authors = helpers.list_authors(session)
        for a, count in authors:
            click.echo(f"{a.name} ({count} books)")


@cli.command("find-author")
@click.argument("name")
def find_author_command(name):
    """Find author"""
    with SessionLocal() as session:
        a = helpers.find_author(session, name)
        click.echo(f"{a.id}: {a.name}")


# Borrowers commands
@cli.command("add-borrower")
@click.argument("name")
@click.argument("contacts")
def add_borrower_command(name, contacts):
    """Add to borrowers list"""
    with SessionLocal() as session:
        helpers.add_borrower(session, name, contacts)
        session.commit()
        click.echo(f"Borrower '{name}' added.")


@cli.command("list-borrowers")
def list_borrowers_command():
    """List borrowers"""
    with SessionLocal() as session:
        borrowers = helpers.list_borrowers(session)
        for b in borrowers:
            click.echo(f"{b.id}: {b.name} ({b.contacts})")


@cli.command("delete-borrower")
@click.argument("borrower_id", type=int)
def delete_borrower_command(borrower_id):
    """Delete borrower"""
    with SessionLocal() as session:
        helpers.delete_borrower(session, borrower_id)
        session.commit()
        click.echo("Borrower deleted.")


# Borrowing
@cli.command("borrow-book")
@click.argument("book_name")
@click.argument("borrower_name")
def borrow_command(book_name, borrower_name):
    """Borrow book"""
    with SessionLocal() as session:
        helpers.borrow(session, book_name, borrower_name)
        session.commit()
        click.echo("Book borrowed.")


@cli.command("return-book")
@click.argument("book_name")
@click.argument("borrower_name")
def return_command(book_name, borrower_name):
    """Return book"""
    with SessionLocal() as session:
        helpers.return_book(session, book_name, borrower_name)
        session.commit()
        click.echo("Book returned.")

#Reports
# REPORT COMMANDS

@cli.command("borrowed-books")
def borrowed_books_command():
    """List all currently borrowed books with borrower names."""
    with SessionLocal() as session:
        records = helpers.get_borrowed_books(session)
        if not records:
            click.echo("No borrowed books.")
        else:
            for r in records:
                click.echo(f"Book: {r.book.title} | Borrower: {r.borrower.name} | Borrowed on: {r.borrow_date}")

@cli.command("history")
@click.argument("book_id", type=int)
def history_command(book_id):
    """Show all past borrowing records for a book."""
    with SessionLocal() as session:
        book = session.query(Book).get(book_id)
        if not book:
            click.echo("Book not found.")
            return
        history = helpers.borrowing_history(session, book)
        if not history:
            click.echo("No history for this book.")
        else:
            for r in history:
                click.echo(f"Borrower: {r.borrower.name} | Borrowed: {r.borrow_date} | Returned: {r.return_date or 'Not returned'}")

@cli.command("late-returns")
@click.option("--days", type=int, default=30, help="Number of days overdue")
def late_returns_command(days):
    """Find overdue books."""
    with SessionLocal() as session:
        late = helpers.late_returns(session, days=days)
        if not late:
            click.echo("No overdue books.")
        else:
            for r in late:
                overdue_days = (datetime.now() - r.borrow_date).days
                click.echo(f"Book: {r.book.title} | Borrower: {r.borrower.name} | Overdue: {overdue_days} days")

@cli.command("top-authors")
@click.option("--number", type=int, default=5, help="Number of top authors to show")
def top_authors_command(number):
    """List authors by number of books."""
    with SessionLocal() as session:
        authors = helpers.top_authors(session, number)
        if not authors:
            click.echo("No authors found.")
        else:
            for a, count in authors:
                click.echo(f"{a.name} ({count} books)")


@cli.command("top-borrowers")
@click.option("--number", type=int, default=5, help="Number of top borrowers to show")
def top_borrowers_command(number):
    """Show top borrowers by borrow count."""
    with SessionLocal() as session:
        borrowers = helpers.top_borrower(session, number)
        if not borrowers:
            click.echo("No borrowers found.")
        else:
            for borrower, borrow_count in borrowers:
                click.echo(f"Borrower: {borrower.name} | Borrowed: {borrow_count} books")


# Menue mode when no arguments are passed

def menu():
    while True:
        print(logo)
        print("1. Add book")
        print("2. List books")
        print("3. Search book")
        print("4. Delete book")
        print("5. Update book")
        print("6. Add author")
        print("7. List authors")
        print("8. Find author")
        print("9. Add borrower")
        print("10. List borrowers")
        print("11. Delete borrower")
        print("12. Borrow book")
        print("13. Return book")
        print("14. Borrowed books")
        print("15. Borrowing history")
        print("16. Late returns")
        print("17. Top authors")
        print("18. Top borrowers")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            with SessionLocal() as session:
                if choice == "1":
                    title = input("Book title: ")
                    author = input("Author: ")
                    year = input("Year (optional): ") or None
                    genre = input("Genre (optional): ") or None
                    helpers.add_book(session, title, author, year, genre)
                    session.commit()
                    print("Book added.")

                elif choice == "2":
                    for b in helpers.list_books(session):
                        print(f"{b.id}: {b.title} by {b.author.name}")

                elif choice == "3":
                    query = input("Search query: ")
                    for b in helpers.search_book(session, query):
                        print(f"{b.id}: {b.title} by {b.author.name}")

                elif choice == "4":
                    bid = int(input("Book ID to delete: "))
                    helpers.delete_book(session, bid)
                    session.commit()
                    print("Book deleted.")

                elif choice == "5":
                    bid = int(input("Book ID to update: "))
                    helpers.update_book(session, bid)
                    session.commit()
                    print("Book updated.")

                elif choice == "6":
                    name = input("Author name: ")
                    birth = input("Birth year: ") or None
                    country = input("Country: ") or None
                    helpers.add_author(session, name, birth, country)
                    session.commit()
                    print("Author added.")

                elif choice == "7":
                    for a, count in helpers.list_authors(session):
                        print(f"{a.name} ({count} books)")

                elif choice == "8":
                    name = input("Author name: ")
                    a = helpers.find_author(session, name)
                    print(f"{a.id}: {a.name}")

                elif choice == "9":
                    name = input("Borrower name: ")
                    contacts = input("Contacts: ")
                    helpers.add_borrower(session, name, contacts)
                    session.commit()
                    print("Borrower added.")

                elif choice == "10":
                    for b in helpers.list_borrowers(session):
                        print(f"{b.id}: {b.name} ({b.contacts})")

                elif choice == "11":
                    bid = int(input("Borrower ID to delete: "))
                    helpers.delete_borrower(session, bid)
                    session.commit()
                    print("Borrower deleted.")

                elif choice == "12":
                    book_name = input("Book name: ")
                    borrower_name = int(input("Borrower name: "))
                    helpers.borrow(session, book_name, borrower_name)
                    session.commit()
                    print("Book borrowed.")

                elif choice == "13":
                    book_name = int(input("Book name: "))
                    borrower_name = int(input("Borrower name: "))
                    helpers.return_book(session, book_name, borrower_name)
                    session.commit()
                    print("Book returned.")

                elif choice == "14":
                    records = helpers.get_borrowed_books(session)
                    if not records:
                        print("No borrowed books.")
                    else:
                        for r in records:
                            print(f"Book: {r.book.title} | Borrower: {r.borrower.name} | Borrowed on: {r.borrow_date}")

                elif choice == "15":
                    book_id = int(input("Enter book ID: "))
                    book = session.query(Book).get(book_id)
                    if not book:
                        print("Book not found.")
                    else:
                        history = helpers.borrowing_history(session, book)
                        if not history:
                            print("No history for this book.")
                        else:
                            for r in history:
                                print(f"Borrower: {r.borrower.name} | Borrowed: {r.borrow_date} | Returned: {r.return_date or 'Not returned'}")

                elif choice == "16":
                    days = input("Days overdue (default 30): ") or "30"
                    late = helpers.late_returns(session, days=int(days))
                    if not late:
                        print("No overdue books.")
                    else:
                        for r in late:
                            overdue_days = (datetime.now() - r.borrow_date).days
                            print(f"Book: {r.book.title} | Borrower: {r.borrower.name} | Overdue: {overdue_days} days")

                elif choice == "17":
                    num = input("Number of authors (default 5): ") or "5"
                    authors = helpers.top_authors(session, int(num))
                    if not authors:
                        print("No authors found.")
                    else:
                        for a, count in authors:
                            print(f"{a.name} ({count} books)")

                elif choice == "18":
                    num = input("Number of borrowers (default 5): ") or "5"
                    borrowers = helpers.top_borrower(session, int(num))
                    if not borrowers:
                        print("No borrowers found.")
                    else:
                        for borrower, borrow_count in borrowers:
                            print(f"Borrower: {borrower.name} | Borrowed: {borrow_count} books")

                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")


#main to run as script

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cli()   
    else:
        menu()  
