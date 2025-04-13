from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class IdolLogEntry(BaseModel):
    timestamp: datetime
    event_type: str
    description: str
    emotion_state: str
    additional_data: Optional[dict] = None

class IdolLog:
    def __init__(self, max_entries: int = 1000):
        self.log_entries: List[IdolLogEntry] = []
        self.max_entries = max_entries
        logger.info("初始化偶像日誌系統")
    
    def add_entry(self, event_type: str, description: str, emotion_state: str, additional_data: Optional[dict] = None) -> None:
        """添加新的日誌條目"""
        entry = IdolLogEntry(
            timestamp=datetime.now(),
            event_type=event_type,
            description=description,
            emotion_state=emotion_state,
            additional_data=additional_data
        )
        
        self.log_entries.append(entry)
        logger.info(f"添加日誌條目: {event_type} - {description}")
        
        # 如果超過最大條目數，移除最舊的條目
        if len(self.log_entries) > self.max_entries:
            self.log_entries.pop(0)
    
    def get_recent_entries(self, limit: int = 10) -> List[IdolLogEntry]:
        """獲取最近的日誌條目"""
        return self.log_entries[-limit:]
    
    def get_entries_by_type(self, event_type: str) -> List[IdolLogEntry]:
        """根據事件類型獲取日誌條目"""
        return [entry for entry in self.log_entries if entry.event_type == event_type]
    
    def get_entries_by_emotion(self, emotion_state: str) -> List[IdolLogEntry]:
        """根據情緒狀態獲取日誌條目"""
        return [entry for entry in self.log_entries if entry.emotion_state == emotion_state]
    
    def get_entries_by_date_range(self, start_date: datetime, end_date: datetime) -> List[IdolLogEntry]:
        """根據日期範圍獲取日誌條目"""
        return [
            entry for entry in self.log_entries
            if start_date <= entry.timestamp <= end_date
        ]
    
    def clear_log(self) -> None:
        """清空日誌"""
        self.log_entries.clear()
        logger.info("清空偶像日誌") 