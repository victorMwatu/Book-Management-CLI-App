from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class BorrowRecords(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    # Foreign Keys
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)

    # Relationships
    book = relationship("Book", back_populates="borrow_records")
    borrower = relationship("Borrower", back_populates="borrow_records")

    def __repr__(self):
        return f"<BorrowRecord(id={self.id}, book_id={self.book_id}, borrower_id={self.borrower_id})>"
