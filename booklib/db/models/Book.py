from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    available = Column(Boolean, default=True)

    # Foreign Key to Authors
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationships
    author = relationship("Author", back_populates="books")
    borrow_records = relationship("BorrowRecords", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', available={self.available})>"
