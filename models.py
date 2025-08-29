from session import engine 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
	pass

class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30))
	
class LoginBase(Base):
	__tablename__ = "login"

	id: Mapped[int] = mapped_column(primary_key=True)
	login: Mapped[str] = mapped_column(String(30))
	password: Mapped[str] = mapped_column(String(30))

Base.metadata.create_all(bind=engine)
