from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func
from role_users.models import Role_userModel

class TrackTimeMixin:

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()

class UserModel(Base , TrackTimeMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50) , unique=True , index= True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer)


# class Permissions(Base):
#     __tablename__ = "permissions"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))