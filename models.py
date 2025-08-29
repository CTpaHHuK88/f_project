from session import engine 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, Integer, String

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

class AuthBase(Base):
    __tablename__ = "auth"
	  
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(20), index=True)
    password = Column(String(255), nullable=False)
    mail = Column(String(50), unique=True, index=True)
    status = Column(Integer)

Base.metadata.create_all(bind=engine)
