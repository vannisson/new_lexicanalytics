from database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    density = Column(Float, nullable=True)
    diversity = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship('User', back_populates='collections')
    productions = relationship(
        'Production', back_populates='collection', lazy=True, cascade="all, delete")
