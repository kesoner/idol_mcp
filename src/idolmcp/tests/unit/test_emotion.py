import pytest
from src.idolmcp.core.emotion import EmotionEngine, EmotionConfig, EmotionState

@pytest.fixture
def sample_emotion_config():
    return EmotionConfig(
        base_emotion=EmotionState.NEUTRAL,
        emotion_triggers={
            "happy": [EmotionState.HAPPY, EmotionState.EXCITED],
            "sad": [EmotionState.SAD],
            "angry": [EmotionState.ANGRY]
        }
    )

@pytest.fixture
def emotion_engine(sample_emotion_config):
    return EmotionEngine(sample_emotion_config)

def test_emotion_initialization(emotion_engine, sample_emotion_config):
    assert emotion_engine.config == sample_emotion_config
    assert emotion_engine.current_state == EmotionState.NEUTRAL
    assert emotion_engine.emotion_intensity == 0.5

def test_update_state(emotion_engine):
    emotion_engine.update_state(EmotionState.HAPPY, 0.8)
    assert emotion_engine.current_state == EmotionState.HAPPY
    assert emotion_engine.emotion_intensity == 0.8

def test_update_state_intensity_bounds(emotion_engine):
    emotion_engine.update_state(EmotionState.HAPPY, 1.5)
    assert emotion_engine.emotion_intensity == 1.0
    
    emotion_engine.update_state(EmotionState.SAD, -0.5)
    assert emotion_engine.emotion_intensity == 0.0

def test_emotion_decay(emotion_engine):
    emotion_engine.update_state(EmotionState.HAPPY, 0.8)
    emotion_engine.decay_emotion()
    assert emotion_engine.emotion_intensity < 0.8
    
    # Test decay to base emotion
    for _ in range(10):
        emotion_engine.decay_emotion()
    assert emotion_engine.current_state == EmotionState.NEUTRAL
    assert emotion_engine.emotion_intensity == 0.5 