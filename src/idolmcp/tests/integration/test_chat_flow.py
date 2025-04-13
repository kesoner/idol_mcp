import pytest
from unittest.mock import AsyncMock, patch
from src.idolmcp.core.persona import Persona, PersonaConfig
from src.idolmcp.core.emotion import EmotionEngine, EmotionConfig, EmotionState
from src.idolmcp.core.memory import MemorySystem, MemoryConfig
from src.idolmcp.core.llm import LLMService, LLMConfig, LLMProvider

@pytest.fixture
def persona_config():
    return PersonaConfig(
        name="星野 琴音",
        style="元氣 / 有點中二 / 喜歡自稱本小姐",
        greeting="嗨嗨！本小姐今天也閃亮登場囉～",
        speech_tone="活潑、感性、帶點誇張",
        likes=["唱歌", "觀察人類", "甜食"],
        memory_tags=["情感", "事件", "粉絲互動"]
    )

@pytest.fixture
def emotion_config():
    return EmotionConfig(
        base_emotion=EmotionState.NEUTRAL,
        emotion_triggers={
            "happy": [EmotionState.HAPPY, EmotionState.EXCITED],
            "sad": [EmotionState.SAD],
            "angry": [EmotionState.ANGRY]
        }
    )

@pytest.fixture
def memory_config():
    return MemoryConfig(
        db_url="sqlite:///:memory:",
        max_memories_per_user=5,
        memory_expiry_days=7
    )

@pytest.fixture
def llm_config():
    return LLMConfig(
        provider=LLMProvider.GEMINI,
        api_key="test_api_key",
        model_name="gemini-pro",
        temperature=0.7,
        max_tokens=1000
    )

@pytest.fixture
def chat_system(persona_config, emotion_config, memory_config, llm_config):
    with patch('google.generativeai.configure'), \
         patch('google.generativeai.GenerativeModel') as mock_model:
        mock_model.return_value.generate_content_async = AsyncMock()
        
        persona = Persona(persona_config)
        emotion_engine = EmotionEngine(emotion_config)
        memory_system = MemorySystem(memory_config)
        llm_service = LLMService(llm_config)
        
        return {
            "persona": persona,
            "emotion_engine": emotion_engine,
            "memory_system": memory_system,
            "llm_service": llm_service
        }

@pytest.mark.asyncio
async def test_complete_chat_flow(chat_system):
    user_id = "test_user"
    user_message = "你好！今天過得怎麼樣？"
    
    # Mock LLM response
    chat_system["llm_service"].model.generate_content_async.return_value.text = "我很好！今天天氣真不錯呢～"
    
    # Process message through the system
    # 1. Update emotion based on message
    chat_system["emotion_engine"].update_state(EmotionState.HAPPY, 0.8)
    
    # 2. Store memory
    chat_system["memory_system"].store_memory(
        user_id,
        user_message,
        ["greeting", "mood"]
    )
    
    # 3. Get persona style
    style = chat_system["persona"].get_response_style()
    
    # 4. Get context from memory
    context = chat_system["memory_system"].get_memories(user_id)
    
    # 5. Generate response
    response = await chat_system["llm_service"].generate_response(
        user_message,
        context=context,
        style=style
    )
    
    # Verify the flow
    assert response == "我很好！今天天氣真不錯呢～"
    assert chat_system["emotion_engine"].current_state == EmotionState.HAPPY
    assert chat_system["emotion_engine"].emotion_intensity == 0.8
    assert len(chat_system["memory_system"].get_memories(user_id)) == 1
    
    # Verify LLM service was called with correct parameters
    chat_system["llm_service"].model.generate_content_async.assert_called_once()
    call_args = chat_system["llm_service"].model.generate_content_async.call_args[0]
    assert user_message in call_args[0]
    assert "Context" in call_args[0]
    assert "Style" in call_args[0] 