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
@click.argument("book_id", type=int)
@click.argument("borrower_id", type=int)
def borrow_command(book_id, borrower_id):
    """Borrow book"""
    with SessionLocal() as session:
        helpers.borrow(session, book_id, borrower_id)
        session.commit()
        click.echo("Book borrowed.")


@cli.command("return-book")
@click.argument("book_id", type=int)
@click.argument("borrower_id", type=int)
def return_command(book_id, borrower_id):
    """Return book"""
    with SessionLocal() as session:
        helpers.return_book(session, book_id, borrower_id)
        session.commit()
        click.echo("Book returned.")

#Reports
@cli.command("top-borrowers")
@click.argument("number", type=int, required=False)
def top_borrowers(number):
    """Show top borrowers. """
    with SessionLocal() as session:
        top_n = helpers.top_borrower(session, number)
        for borrower, borrow_count in top_n:
            click.echo(f'ID: {borrower.id}:, {borrower.name}, Borrowed: {borrow_count}')




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
        print("14. Top borrowers")
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
                    book_name = int(input("Book name: "))
                    borrower_name = int(input("Borrower name: "))
                    helpers.borrow(session, book_name, borrower_name)
                    session.commit()
                    print("Book borrowed.")

                elif choice == "13":
                    book_id = int(input("Book ID: "))
                    borrower_id = int(input("Borrower ID: "))
                    helpers.return_book(session, book_id, borrower_id)
                    session.commit()
                    print("Book returned.")

                elif choice == "14":
                    for borrower, borrow_count in helpers.top_borrower(session, number):
                        print(f'ID: {borrower.id}:, {borrower.name}, Borrowed: {borrow_count}')

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
