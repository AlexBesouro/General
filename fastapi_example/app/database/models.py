import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID, JSON


class Base(DeclarativeBase):  # ---- BASE CLASS FOR ALL MODELS
    pass


class ThoughtAlchemy(Base):  # ---- SQLALCHEMY MODEL that maps to the database table
    __tablename__ = "thoughts"

    id: Mapped[uuid.UUID] = mapped_column(  # Mapped describes a mapped attribute
        # mapped_column describes how the attribute maps to a database column
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str]  # No mapped_column means default mapping
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(
        # server_default cant be used with mapped without mapped_column
        Boolean, server_default="TRUE")
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"))
    owner = relationship("UserAlchemy")


class UserAlchemy(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"))
