from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from db.database import Base

class ChatHistory(Base):
    __tablename__ = "chat history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default = func.now()
    )
