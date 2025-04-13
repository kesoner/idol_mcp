from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    content = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MemoryConfig(BaseModel):
    db_url: str
    max_memories_per_user: int = 100
    memory_expiry_days: int = 30

class MemorySystem:
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.engine = create_engine(config.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_memory(self, user_id: str, content: str, tags: List[str]) -> None:
        """Store a new memory entry."""
        session = self.Session()
        try:
            memory = MemoryEntry(
                user_id=user_id,
                content=content,
                tags=tags
            )
            session.add(memory)
            session.commit()
        finally:
            session.close()
    
    def get_memories(self, user_id: str, tags: Optional[List[str]] = None) -> List[Dict]:
        """Retrieve memories for a user, optionally filtered by tags."""
        session = self.Session()
        try:
            # Get all memories for the user
            memories = session.query(MemoryEntry).filter(
                MemoryEntry.user_id == user_id
            ).order_by(
                MemoryEntry.updated_at.desc()
            ).all()
            
            # Filter memories by tags in Python
            if tags:
                filtered_memories = []
                for memory in memories:
                    # Check if all requested tags are present in memory tags
                    if all(tag in memory.tags for tag in tags):
                        filtered_memories.append(memory)
                memories = filtered_memories[:self.config.max_memories_per_user]
            else:
                memories = memories[:self.config.max_memories_per_user]
            
            return [{"content": m.content, "tags": m.tags, "created_at": m.created_at} for m in memories]
        finally:
            session.close()
    
    def cleanup_old_memories(self) -> None:
        """Remove memories older than the configured expiry period."""
        session = self.Session()
        try:
            expiry_date = datetime.utcnow() - timedelta(days=self.config.memory_expiry_days)
            session.query(MemoryEntry).filter(MemoryEntry.created_at < expiry_date).delete()
            session.commit()
        finally:
            session.close() 