
from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.models.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (UniqueConstraint('user_id', 'campaign_id', name='_user_campaign_uc'),)
