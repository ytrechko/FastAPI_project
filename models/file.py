from database.session import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    uploadet_at: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
