from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    email: Mapped[str] = mapped_column(String, unique = True, index = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(String, nullable = False)
    role: Mapped[str] = mapped_column(String, nullable = False)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True, nullable = False)
