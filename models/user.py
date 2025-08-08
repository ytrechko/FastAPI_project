from database.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.file import File


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)

    files: Mapped[list["File"]] = relationship("File", backref="owners")
