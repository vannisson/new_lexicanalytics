from database import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid


class Production(Base):
    __tablename__ = 'productions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id'))

    collection = relationship('Collection', back_populates='productions')

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "text": self.text,
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            "collection_id": str(self.collection_id)
        }