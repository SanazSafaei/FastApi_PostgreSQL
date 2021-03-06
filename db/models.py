from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from db.postgresql_db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Integer, ForeignKey("roles.id"), default = 2)

    log = relationship("Log", back_populates="owner")

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key = True, index = True)
    role_name = Column(String, unique = True, index = True )

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    request = Column(String, index=True)
    response = Column(JSON, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="log")