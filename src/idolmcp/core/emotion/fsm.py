from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class EmotionState(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    EXCITED = "excited"
    SAD = "sad"
    ANGRY = "angry"
    SHY = "shy"
    CONFIDENT = "confident"

class EmotionTransition(BaseModel):
    from_state: EmotionState
    to_state: EmotionState
    trigger: str
    probability: float = 1.0
    conditions: Optional[Dict] = None

class EmotionFSM:
    def __init__(self, initial_state: EmotionState = EmotionState.NEUTRAL):
        self.current_state = initial_state
        self.transitions: Dict[EmotionState, List[EmotionTransition]] = {}
        self._setup_default_transitions()
        logger.info(f"初始化情緒 FSM，初始狀態: {initial_state.value}")
    
    def _setup_default_transitions(self):
        """設置默認的情緒轉換規則"""
        # 從中性狀態的轉換
        self.add_transition(
            EmotionTransition(
                from_state=EmotionState.NEUTRAL,
                to_state=EmotionState.HAPPY,
                trigger="positive_interaction",
                probability=0.8
            )
        )
        self.add_transition(
            EmotionTransition(
                from_state=EmotionState.NEUTRAL,
                to_state=EmotionState.SAD,
                trigger="negative_interaction",
                probability=0.7
            )
        )
        
        # 從開心狀態的轉換
        self.add_transition(
            EmotionTransition(
                from_state=EmotionState.HAPPY,
                to_state=EmotionState.EXCITED,
                trigger="exciting_event",
                probability=0.6
            )
        )
        
        # 從悲傷狀態的轉換
        self.add_transition(
            EmotionTransition(
                from_state=EmotionState.SAD,
                to_state=EmotionState.NEUTRAL,
                trigger="comfort",
                probability=0.5
            )
        )
    
    def add_transition(self, transition: EmotionTransition):
        """添加新的情緒轉換規則"""
        if transition.from_state not in self.transitions:
            self.transitions[transition.from_state] = []
        self.transitions[transition.from_state].append(transition)
        logger.debug(f"添加轉換規則: {transition.from_state.value} -> {transition.to_state.value}")
    
    def process_trigger(self, trigger: str, context: Optional[Dict] = None) -> bool:
        """處理觸發事件，可能導致狀態轉換"""
        logger.info(f"處理觸發事件: {trigger}, 當前狀態: {self.current_state.value}")
        
        if self.current_state not in self.transitions:
            logger.warning(f"當前狀態 {self.current_state.value} 沒有定義轉換規則")
            return False
        
        for transition in self.transitions[self.current_state]:
            if transition.trigger == trigger:
                # 檢查條件
                if transition.conditions and not self._check_conditions(transition.conditions, context):
                    continue
                
                # 根據概率決定是否轉換
                if self._should_transition(transition.probability):
                    logger.info(f"狀態轉換: {self.current_state.value} -> {transition.to_state.value}")
                    self.current_state = transition.to_state
                    return True
        
        logger.debug(f"沒有找到合適的轉換規則")
        return False
    
    def _check_conditions(self, conditions: Dict, context: Optional[Dict]) -> bool:
        """檢查轉換條件是否滿足"""
        if not context:
            return False
        
        for key, value in conditions.items():
            if key not in context or context[key] != value:
                return False
        return True
    
    def _should_transition(self, probability: float) -> bool:
        """根據概率決定是否進行狀態轉換"""
        import random
        return random.random() < probability
    
    def get_current_state(self) -> EmotionState:
        """獲取當前情緒狀態"""
        return self.current_state 