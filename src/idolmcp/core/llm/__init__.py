from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class LLMProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"

class LLMConfig(BaseModel):
    provider: LLMProvider
    api_key: str
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000

class LLMService:
    def __init__(self, config: LLMConfig):
        self.config = config
        self._setup_provider()
    
    def _setup_provider(self) -> None:
        """Initialize the LLM provider based on configuration."""
        if self.config.provider == LLMProvider.GEMINI:
            try:
                logger.info(f"初始化 Gemini API，使用模型: {self.config.model_name}")
                genai.configure(api_key=self.config.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.config.model_name
                )
                logger.info("Gemini API 初始化成功")
            except Exception as e:
                logger.error(f"初始化 Gemini API 時發生錯誤: {str(e)}")
                raise
        elif self.config.provider == LLMProvider.OPENAI:
            # TODO: Implement OpenAI integration
            pass
    
    async def generate_response(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        style: Optional[Dict] = None
    ) -> str:
        """Generate a response using the configured LLM provider."""
        if self.config.provider == LLMProvider.GEMINI:
            try:
                logger.info("開始生成回應...")
                formatted_prompt = self.format_prompt(prompt, context, style)
                logger.debug(f"格式化後的提示詞: {formatted_prompt}")
                
                response = await self.model.generate_content_async(
                    formatted_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.config.temperature,
                        max_output_tokens=self.config.max_tokens,
                    )
                )
                
                if not response.text:
                    raise Exception("回應為空")
                
                logger.info("回應生成成功")
                return response.text
            except Exception as e:
                logger.error(f"生成回應時發生錯誤: {str(e)}")
                raise Exception(f"Error generating response: {str(e)}")
        elif self.config.provider == LLMProvider.OPENAI:
            # TODO: Implement OpenAI response generation
            pass
    
    def format_prompt(
        self,
        user_message: str,
        context: Optional[Dict] = None,
        style: Optional[Dict] = None
    ) -> str:
        """Format the prompt with context and style information."""
        prompt_parts = []
        
        if context:
            prompt_parts.append(f"Context: {context}")
        
        if style:
            prompt_parts.append(f"Style: {style}")
        
        prompt_parts.append(f"User: {user_message}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts) 