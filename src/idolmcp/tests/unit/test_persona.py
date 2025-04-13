import pytest
from src.idolmcp.core.persona import Persona, PersonaConfig

@pytest.fixture
def sample_persona_config():
    return PersonaConfig(
        name="星野 琴音",
        style="元氣 / 有點中二 / 喜歡自稱本小姐",
        greeting="嗨嗨！本小姐今天也閃亮登場囉～",
        speech_tone="活潑、感性、帶點誇張",
        likes=["唱歌", "觀察人類", "甜食"],
        memory_tags=["情感", "事件", "粉絲互動"]
    )

@pytest.fixture
def persona(sample_persona_config):
    return Persona(sample_persona_config)

def test_persona_initialization(persona, sample_persona_config):
    assert persona.config == sample_persona_config
    assert persona.current_mood == "neutral"

def test_get_response_style(persona):
    style = persona.get_response_style()
    assert isinstance(style, dict)
    assert "tone" in style
    assert "mood" in style
    assert "style" in style
    assert style["mood"] == "neutral"

def test_adjust_mood(persona):
    persona.adjust_mood("happy")
    assert persona.current_mood == "happy"
    style = persona.get_response_style()
    assert style["mood"] == "happy" 