# Book Management CLI App

A command-line application for cataloguing and managing a personal book collection. This application provides a complete solution for tracking books, authors, borrowers, and borrowing history through an intuitive CLI interface with SQLite database persistence.

## Features

### Books Management
- Add new books with complete metadata (title, author, year, genre)
- List all books with availability status
- Search books by title, author, or genre
- Update book information
- Delete books from collection

### Author Management
- Register new authors with biographical information
- View authors and their book counts
- Search authors by name

### Borrower Management
- Register borrowers with contact information
- View all registered borrowers
- Remove borrowers from system

### Borrowing System
- Borrow books with automatic availability tracking
- Return books with date logging
- Complete borrowing history maintenance

### Reports & Analytics
- View currently borrowed books
- Track borrowing history for any book
- Find overdue books
- Analyze top authors and borrowers

## Tech Stack

- **Database**: SQLite with SQLAlchemy ORM
- **CLI Framework**: Click
- **Migrations**: Alembic
- **Language**: Python 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- pipenv (recommended) or pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-management-cli
   ```

2. **Install dependencies using pipenv (recommended)**
   ```bash
   pipenv install
   pipenv shell
   ```

   **Or using pip**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   alembic upgrade head
   ```

## Usage

### Books Management

```bash
# Add a new book
booklib add-book

# List all books
booklib list-books

# Search for books
booklib search-book --title "Dune"
booklib search-book --author "Asimov"
booklib search-book --genre "Science Fiction"

# Update book information
booklib update-book <book_id>

# Delete a book
booklib delete-book <book_id>
```

### Author Management

```bash
# Add a new author
booklib add-author

# List all authors
booklib list-authors

# Find author by name
booklib find-author --name "Asimov"
```

### Borrower Management

```bash
# Register a new borrower
booklib add-borrower

# List all borrowers
booklib list-borrowers

# Remove a borrower
booklib delete-borrower <borrower_id>
```

### Borrowing Operations

```bash
# Borrow a book
booklib borrow <book_id> --by <borrower_id>

# Return a book
booklib return <book_id>
```

### Reports and Queries

```bash
# View currently borrowed books
booklib borrowed-books

# View borrowing history for a book
booklib history <book_id>

# Find overdue books (default 30 days)
booklib late-returns --days 30

# View top authors by book count
booklib top-authors

# View top borrowers by borrowing frequency
booklib top-borrowers
```

## Database Schema

### Books Table
- `id` (Primary Key)
- `title`
- `author_id` (Foreign Key → Authors.id)
- `year`
- `genre`
- `available` (Boolean, default True)

### Authors Table
- `id` (Primary Key)
- `name`
- `birth_year` (Optional)
- `country` (Optional)

### Borrowers Table
- `id` (Primary Key)
- `name`
- `email` (Optional)

### BorrowRecords Table
- `id` (Primary Key)
- `book_id` (Foreign Key → Books.id)
- `borrower_id` (Foreign Key → Borrowers.id)
- `borrow_date`
- `return_date` (Nullable)

## Project Structure

```
.
├── Pipfile                # Python dependencies for pipenv
├── Pipfile.lock           # Locked dependency versions
├── README.md              # Project documentation
├── alembic.ini            # Alembic configuration
├── booklib/               # Main application package
│   ├── __init__.py
│   ├── cli.py             # CLI entry point and commands
│   ├── db/                # Database layer
│   │   ├── __init__.py
│   │   ├── database.py    # SQLAlchemy engine and session setup
│   │   └── models/        # ORM model definitions
│   │       ├── __init__.py
│   │       ├── base.py    # Base declarative class
│   │       ├── Author.py
│   │       ├── Book.py
│   │       ├── Borrower.py
│   │       └── BorrowRecords.py
│   └── helpers.py         # Utility functions
└── migrations/            # Alembic migration scripts
    ├── README
    ├── env.py
    ├── script.py.mako
    └── versions/
```

## Development

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Adding New Features

1. Update models in `booklib/db/models/`
2. Create migration: `alembic revision --autogenerate -m "Add new feature"`
3. Apply migration: `alembic upgrade head`
4. Update CLI commands in `booklib/cli.py`
5. Add helper functions in `booklib/helpers.py` if needed

## Data Structures Used

- **Lists**: Store database query results and collections
- **Dictionaries**: Handle database records and query parameters
- **Tuples**: Manage database query results and immutable data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Database not found**: Run `alembic upgrade head` to initialize the database

**Import errors**: Ensure you're in the correct virtual environment (`pipenv shell`)

**Permission errors**: Check file permissions in the project directory

## Future Enhancements

- Web interface using Flask
- Export/import functionality (CSV, JSON)
- Advanced search with filters
- Email notifications for overdue books
- Book recommendations system
- Barcode scanning support

---

## License

MIT License

Copyright (c) 2025 [Victor Nzioka Mwatu]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.