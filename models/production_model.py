from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Production(Base):
    __tablename__ = 'productions'
    id = Column(UUID(as_uuid=True), name="uuid", primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)