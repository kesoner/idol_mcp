import pytest
from datetime import datetime, timedelta
from src.idolmcp.core.memory import MemorySystem, MemoryConfig, MemoryEntry

@pytest.fixture
def memory_config():
    return MemoryConfig(
        db_url="sqlite:///:memory:",
        max_memories_per_user=5,
        memory_expiry_days=7
    )

@pytest.fixture
def memory_system(memory_config):
    system = MemorySystem(memory_config)
    yield system
    # Cleanup after tests
    system.engine.dispose()

def test_store_memory(memory_system):
    user_id = "test_user"
    content = "Test memory content"
    tags = ["test", "memory"]
    
    memory_system.store_memory(user_id, content, tags)
    memories = memory_system.get_memories(user_id)
    
    assert len(memories) == 1
    assert memories[0]["content"] == content
    assert memories[0]["tags"] == tags

def test_get_memories_with_tags(memory_system):
    user_id = "test_user"
    
    # Store multiple memories with different tags
    memory_system.store_memory(user_id, "Memory 1", ["tag1"])
    memory_system.store_memory(user_id, "Memory 2", ["tag2"])
    memory_system.store_memory(user_id, "Memory 3", ["tag1", "tag2"])
    
    # Test filtering by single tag
    memories = memory_system.get_memories(user_id, ["tag1"])
    assert len(memories) == 2
    
    # Test filtering by multiple tags
    memories = memory_system.get_memories(user_id, ["tag1", "tag2"])
    assert len(memories) == 1

def test_memory_limit(memory_system):
    user_id = "test_user"
    
    # Store more memories than the limit
    for i in range(10):
        memory_system.store_memory(user_id, f"Memory {i}", ["test"])
    
    memories = memory_system.get_memories(user_id)
    assert len(memories) == memory_system.config.max_memories_per_user

def test_cleanup_old_memories(memory_system):
    user_id = "test_user"
    
    # Store a memory that should be kept
    memory_system.store_memory(user_id, "Recent memory", ["test"])
    
    # Store a memory that should be cleaned up
    old_memory = MemoryEntry(
        user_id=user_id,
        content="Old memory",
        tags=["test"],
        created_at=datetime.utcnow() - timedelta(days=10)
    )
    session = memory_system.Session()
    session.add(old_memory)
    session.commit()
    session.close()
    
    memory_system.cleanup_old_memories()
    memories = memory_system.get_memories(user_id)
    
    assert len(memories) == 1
    assert memories[0]["content"] == "Recent memory" 