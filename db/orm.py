from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from api.request_status_enum import RequestStatusEnum
import sqlalchemy  # import Enum
from contextlib import contextmanager

from typing import List
from sqlalchemy import Integer, String, UUID, DateTime
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, nullable=False, unique=True)

    uploads: Mapped[List["Upload"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = "upload"
    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(String)  # TODO
    filename = mapped_column(String, nullable=False)
    upload_time = mapped_column(DateTime)
    finish_time = mapped_column(DateTime)
    status = mapped_column(sqlalchemy.Enum(RequestStatusEnum))  # TODO - does not work as expected
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="uploads")


class Singleton(type):
    """
    Taken from https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=Singleton):
    """
    Database singleton class to manage the operations.
    """
    def __init__(self):  # TODO
        """
        Initialize the database
        """
        self.engine = engine = create_engine(
            "sqlite:///C:\\Users\\shake\\Desktop\\College\\4th Year\\Semester B\\Excellenteam\\python\\Ex\\final-exercise-shakedva\\db\\example.db"
        )
        Base.metadata.create_all(bind=engine)

    @contextmanager
    def session(self):
        """
        Context manager for creating a database session.
        :yield: the session
        """
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            yield session

    def drop_all_rows_tables(self):
        """
        Drops all rows from User and Upload tables.
        """
        with self.session() as session:
            session.query(User).delete()
            session.query(Upload).delete()
            session.commit()
