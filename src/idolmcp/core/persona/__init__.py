from typing import Dict, List, Optional
from pydantic import BaseModel

class PersonaConfig(BaseModel):
    name: str
    style: str
    greeting: str
    speech_tone: str
    likes: List[str]
    memory_tags: List[str]

class Persona:
    def __init__(self, config: PersonaConfig):
        self.config = config
        self.current_mood: str = "neutral"
    
    def get_response_style(self) -> Dict[str, str]:
        """Get the current response style based on mood and persona config."""
        return {
            "tone": self.config.speech_tone,
            "mood": self.current_mood,
            "style": self.config.style
        }
    
    def adjust_mood(self, mood: str) -> None:
        """Adjust the persona's current mood."""
        self.current_mood = mood 