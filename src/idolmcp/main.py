import asyncio
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
import logging
import traceback

from core.persona import Persona, PersonaConfig
from core.emotion import EmotionEngine, EmotionConfig, EmotionState
from core.memory import MemorySystem, MemoryConfig
from core.llm import LLMService, LLMConfig, LLMProvider

# 配置日誌
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    platform: str

class ChatResponse(BaseModel):
    response: str
    emotion: str
    emotion_intensity: float

class IdolMCP:
    def __init__(self):
        try:
            logger.info("初始化 IdolMCP 配置...")
            # Initialize configurations
            self.persona_config = PersonaConfig(
                name=os.getenv("PERSONA_NAME", "星野 琴音"),
                style=os.getenv("PERSONA_STYLE", "元氣 / 有點中二 / 喜歡自稱本小姐"),
                greeting=os.getenv("PERSONA_GREETING", "嗨嗨！本小姐今天也閃亮登場囉～"),
                speech_tone=os.getenv("PERSONA_TONE", "活潑、感性、帶點誇張"),
                likes=os.getenv("PERSONA_LIKES", "唱歌,觀察人類,甜食").split(","),
                memory_tags=os.getenv("PERSONA_MEMORY_TAGS", "情感,事件,粉絲互動").split(",")
            )
            logger.info("Persona 配置完成")
            
            self.emotion_config = EmotionConfig(
                base_emotion=EmotionState.NEUTRAL,
                emotion_triggers={
                    "happy": [EmotionState.HAPPY, EmotionState.EXCITED],
                    "sad": [EmotionState.SAD],
                    "angry": [EmotionState.ANGRY]
                }
            )
            logger.info("Emotion 配置完成")
            
            self.memory_config = MemoryConfig(
                db_url=os.getenv("DATABASE_URL", "sqlite:///idolmcp.db"),
                max_memories_per_user=int(os.getenv("MAX_MEMORIES", "100")),
                memory_expiry_days=int(os.getenv("MEMORY_EXPIRY_DAYS", "30"))
            )
            logger.info("Memory 配置完成")
            
            self.llm_config = LLMConfig(
                provider=LLMProvider[os.getenv("LLM_PROVIDER", "GEMINI")],
                api_key=os.getenv("LLM_API_KEY"),
                model_name=os.getenv("LLM_MODEL", "gemini-pro"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000"))
            )
            logger.info("LLM 配置完成")
            
            # Initialize components
            logger.info("初始化組件...")
            self.persona = Persona(self.persona_config)
            self.emotion_engine = EmotionEngine(self.emotion_config)
            self.memory_system = MemorySystem(self.memory_config)
            self.llm_service = LLMService(self.llm_config)
            logger.info("所有組件初始化完成")
            
            # Initialize FastAPI app
            self.app = FastAPI(title="IdolMCP API")
            
            # 添加 CORS 中間件
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["http://localhost:5173", "http://localhost:5174"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            self._setup_routes()
            logger.info("FastAPI 路由設置完成")
            
        except Exception as e:
            logger.error(f"初始化過程中發生錯誤: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _setup_routes(self):
        @self.app.post("/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest):
            try:
                logger.info(f"收到聊天請求: {request}")
                
                # Process message through the system
                logger.info("更新情緒狀態...")
                self.emotion_engine.update_state(EmotionState.HAPPY, 0.8)
                
                logger.info("存儲記憶...")
                self.memory_system.store_memory(
                    request.user_id,
                    request.message,
                    ["chat", request.platform]
                )
                
                logger.info("獲取角色風格...")
                style = self.persona.get_response_style()
                
                logger.info("獲取記憶上下文...")
                context = self.memory_system.get_memories(request.user_id)
                
                logger.info("生成回應...")
                response = await self.llm_service.generate_response(
                    request.message,
                    context=context,
                    style=style
                )
                
                logger.info("回應生成完成")
                return ChatResponse(
                    response=response,
                    emotion=self.emotion_engine.current_state.value,
                    emotion_intensity=self.emotion_engine.emotion_intensity
                )
            except Exception as e:
                logger.error(f"處理聊天請求時發生錯誤: {str(e)}")
                logger.error(traceback.format_exc())
                raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("啟動 IdolMCP 服務...")
    idolmcp = IdolMCP()
    uvicorn.run(idolmcp.app, host="0.0.0.0", port=8002, log_level="debug") 