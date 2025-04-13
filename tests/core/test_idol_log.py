import pytest
from datetime import datetime, timedelta
from src.idolmcp.core.idol_log import IdolLog, IdolLogEntry

def test_add_entry():
    log = IdolLog()
    log.add_entry(
        event_type="training",
        description="舞蹈練習",
        emotion_state="happy",
        additional_data={"duration": 60}
    )
    assert len(log.log_entries) == 1
    entry = log.log_entries[0]
    assert entry.event_type == "training"
    assert entry.description == "舞蹈練習"
    assert entry.emotion_state == "happy"
    assert entry.additional_data["duration"] == 60

def test_get_recent_entries():
    log = IdolLog()
    for i in range(15):
        log.add_entry(
            event_type=f"event_{i}",
            description=f"description_{i}",
            emotion_state="neutral"
        )
    
    recent_entries = log.get_recent_entries(limit=10)
    assert len(recent_entries) == 10
    assert recent_entries[0].event_type == "event_5"
    assert recent_entries[-1].event_type == "event_14"

def test_get_entries_by_type():
    log = IdolLog()
    log.add_entry("training", "舞蹈練習", "happy")
    log.add_entry("performance", "演唱會", "excited")
    log.add_entry("training", "聲樂練習", "neutral")
    
    training_entries = log.get_entries_by_type("training")
    assert len(training_entries) == 2
    assert all(entry.event_type == "training" for entry in training_entries)

def test_get_entries_by_emotion():
    log = IdolLog()
    log.add_entry("event1", "desc1", "happy")
    log.add_entry("event2", "desc2", "sad")
    log.add_entry("event3", "desc3", "happy")
    
    happy_entries = log.get_entries_by_emotion("happy")
    assert len(happy_entries) == 2
    assert all(entry.emotion_state == "happy" for entry in happy_entries)

def test_get_entries_by_date_range():
    log = IdolLog()
    now = datetime.now()
    
    # 添加不同時間的條目
    log.add_entry("event1", "desc1", "neutral")
    log.add_entry("event2", "desc2", "neutral")
    
    # 獲取最近一小時的條目
    start_date = now - timedelta(hours=1)
    end_date = now + timedelta(hours=1)
    entries = log.get_entries_by_date_range(start_date, end_date)
    assert len(entries) == 2

def test_max_entries_limit():
    log = IdolLog(max_entries=5)
    for i in range(10):
        log.add_entry(f"event_{i}", f"desc_{i}", "neutral")
    
    assert len(log.log_entries) == 5
    assert log.log_entries[0].event_type == "event_5"
    assert log.log_entries[-1].event_type == "event_9"

def test_clear_log():
    log = IdolLog()
    log.add_entry("event1", "desc1", "neutral")
    log.add_entry("event2", "desc2", "neutral")
    
    log.clear_log()
    assert len(log.log_entries) == 0 