from src.idolmcp.core.memory import Base, MemoryConfig, MemorySystem
from dotenv import load_dotenv
import os

load_dotenv()

# 創建記憶系統配置
config = MemoryConfig(
    db_url=os.getenv("DATABASE_URL", "sqlite:///idolmcp.db"),
    max_memories_per_user=int(os.getenv("MAX_MEMORIES", "100")),
    memory_expiry_days=int(os.getenv("MEMORY_EXPIRY_DAYS", "30"))
)

# 初始化記憶系統（這會自動創建資料庫和表）
memory_system = MemorySystem(config)

print("資料庫初始化完成！") 