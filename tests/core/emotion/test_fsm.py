import pytest
from src.idolmcp.core.emotion.fsm import EmotionFSM, EmotionState, EmotionTransition

def test_initial_state():
    fsm = EmotionFSM()
    assert fsm.get_current_state() == EmotionState.NEUTRAL

def test_positive_interaction():
    fsm = EmotionFSM()
    # 由於有概率因素，我們需要多次測試
    transitions = 0
    for _ in range(100):
        if fsm.process_trigger("positive_interaction"):
            transitions += 1
    assert transitions > 0  # 應該至少發生一次轉換
    assert fsm.get_current_state() in [EmotionState.HAPPY, EmotionState.NEUTRAL]

def test_negative_interaction():
    fsm = EmotionFSM()
    transitions = 0
    for _ in range(100):
        if fsm.process_trigger("negative_interaction"):
            transitions += 1
    assert transitions > 0
    assert fsm.get_current_state() in [EmotionState.SAD, EmotionState.NEUTRAL]

def test_conditional_transition():
    fsm = EmotionFSM()
    # 添加一個有條件的轉換
    fsm.add_transition(
        EmotionTransition(
            from_state=EmotionState.NEUTRAL,
            to_state=EmotionState.CONFIDENT,
            trigger="special_event",
            probability=1.0,
            conditions={"user_type": "vip"}
        )
    )
    
    # 不滿足條件的情況
    assert not fsm.process_trigger("special_event", {"user_type": "normal"})
    assert fsm.get_current_state() == EmotionState.NEUTRAL
    
    # 滿足條件的情況
    assert fsm.process_trigger("special_event", {"user_type": "vip"})
    assert fsm.get_current_state() == EmotionState.CONFIDENT

def test_invalid_trigger():
    fsm = EmotionFSM()
    assert not fsm.process_trigger("invalid_trigger")
    assert fsm.get_current_state() == EmotionState.NEUTRAL

def test_state_sequence():
    fsm = EmotionFSM()
    # 測試一系列狀態轉換
    fsm.process_trigger("positive_interaction")
    assert fsm.get_current_state() == EmotionState.HAPPY
    
    fsm.process_trigger("exciting_event")
    assert fsm.get_current_state() == EmotionState.EXCITED 