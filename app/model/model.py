from sqlalchemy import Column, String, Boolean, Integer

from app.database.database import Base


class Test(Base):

    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"hashed_password=\"{self.hashed_password}\", " \
               f"is_active={self.is_active})>"