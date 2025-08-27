from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=True)
    country = Column(String, nullable=True)

    # Relationships
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
