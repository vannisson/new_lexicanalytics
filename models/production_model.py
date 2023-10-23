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
    n_lines = Column(Integer, nullable=False)
    n_tokens = Column(Integer, nullable=False)
    n_types = Column(Integer, nullable=False)
    ure_density = Column(Float)
    halliday_density = Column(Float)
    ttr_diversity = Column(Float)
    rttr_diversity = Column(Float)
    cttr_diversity = Column(Float)
    msttr_diversity = Column(Float)
    mattr_diversity = Column(Float)
    mtld_diversity = Column(Float)
    hdd_diversity = Column(Float)
    vocd_diversity = Column(Float)
    herdan_diversity = Column(Float)
    summer_diversity = Column(Float)
    dugast_diversity = Column(Float)
    maas_diversity = Column(Float)
    word_frequency = Column(JSONB) 
    word_tagged = Column(JSONB) 
    lexical_items = Column(JSONB) 
    non_lexical_items = Column(JSONB) 

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id'))

    collection = relationship('Collection', back_populates='productions')

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "text": self.text,
            "n_lines": self.n_lines,
            "n_tokens": self.n_tokens,
            "n_types": self.n_types,
            "ure_density": self.ure_density,
            "halliday_density": self.halliday_density,
            "ttr_diversity": self.ttr_diversity,
            "rttr_diversity": self.rttr_diversity,
            "cttr_diversity": self.cttr_diversity,
            "msttr_diversity": self.msttr_diversity,
            "mattr_diversity": self.mattr_diversity,
            "mtld_diversity": self.mtld_diversity,
            "hdd_diversity": self.hdd_diversity,
            "vocd_diversity": self.vocd_diversity,
            "herdan_diversity": self.herdan_diversity,
            "summer_diversity": self.summer_diversity,
            "dugast_diversity": self.dugast_diversity,
            "maas_diversity": self.maas_diversity,
            "word_frequency": self.word_frequency,
            "word_tagged": self.word_tagged,
            "lexical_items": self.lexical_items,
            "non_lexical_items": self.non_lexical_items,
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            "collection_id": str(self.collection_id)
        }