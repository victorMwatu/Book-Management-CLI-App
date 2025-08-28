from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship

class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contacts = Column(String, nullable=False)

    # Relationships
    borrow_records = relationship("BorrowRecords", back_populates="borrower")

    def __repr__(self):
        return f"<Borrower(id={self.id}, name='{self.name}')>"
