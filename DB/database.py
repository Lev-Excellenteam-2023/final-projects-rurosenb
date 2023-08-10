from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


# Define the database file path
print(os.getenv('DB_FOLDER_PATH'))
print(os.path.join(os.getenv('DB_FOLDER_PATH'), "gpt_explainer.db"))
DB_PATH = os.path.join(os.getenv('DB_FOLDER_PATH'), "gpt_explainer.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    uploads = relationship("Upload", back_populates="user")


class Upload(Base):
    __tablename__ = 'uploads'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime)
    finish_time = Column(DateTime)
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="uploads")


# Create tables in the database
Base.metadata.create_all(engine)
