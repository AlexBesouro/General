from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


class Base(DeclarativeBase):  # ---- BASE CLASS FOR ALL MODELS
    pass


class ThoughtAlchemy(Base):  # ---- SQLALCHEMY MODEL that maps to the database table
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("NOW()"))
