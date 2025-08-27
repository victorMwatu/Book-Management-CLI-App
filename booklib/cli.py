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
    # Always show the logo first
    click.echo(logo)

    # If no subcommand given → show default help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command("add-book")
@click.option("--title", prompt="Book title")
@click.option("--author", prompt="Author name")
@click.option("--year", type=int, prompt="Year", required=False)
@click.option("--genre", prompt="Genre", required=False)
def add_book_command(title, author, year, genre):
    """Add a new book to the library"""
    try:
        with SessionLocal() as session:
            helpers.add_book(session, title, author, year, genre)
            session.commit()
            click.echo(f"Book '{title}' by {author} added.")
    except SQLAlchemyError as e:
        click.echo(f"Database error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)


@cli.command("list-books")
def list_books_command():
    """Show all books in the library"""
    try:
        with SessionLocal() as session:
            books = helpers.list_books(session)
            if not books:
                click.echo("No books found.")
            else:
                for book in books:
                    click.echo(f"{book.id}: {book.title} by {book.author.name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()