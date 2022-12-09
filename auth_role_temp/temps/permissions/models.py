from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func


class TrackTimeMixin:

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()


class PermissionModel(Base , TrackTimeMixin):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    label = Column(String(50))
    