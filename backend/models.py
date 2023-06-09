from sqlalchemy import Column, Boolean, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBtable(Base):
    __tablename__ = "userInfo"

    username = Column(VARCHAR, nullable=False, primary_key=True)
    hashed_password = Column(VARCHAR, nullable=False)
    userType = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False)
    profilePicture = Column(VARCHAR, nullable=True)
    text = Column(VARCHAR, nullable=True)
    disabled = Column(Boolean, nullable=False)