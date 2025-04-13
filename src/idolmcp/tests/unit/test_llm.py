import pytest
from unittest.mock import AsyncMock, patch
from src.idolmcp.core.llm import LLMService, LLMConfig, LLMProvider

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
def llm_service(llm_config):
    with patch('google.generativeai.configure') as mock_configure, \
         patch('google.generativeai.GenerativeModel') as mock_model:
        mock_model.return_value.generate_content_async = AsyncMock()
        service = LLMService(llm_config)
        yield service

@pytest.mark.asyncio
async def test_generate_response(llm_service):
    test_prompt = "Hello, how are you?"
    expected_response = "I'm doing well, thank you!"
    
    llm_service.model.generate_content_async.return_value.text = expected_response
    
    response = await llm_service.generate_response(test_prompt)
    assert response == expected_response
    
    llm_service.model.generate_content_async.assert_called_once_with(
        test_prompt,
        generation_config={
            "temperature": llm_service.config.temperature,
            "max_output_tokens": llm_service.config.max_tokens,
        }
    )

def test_format_prompt(llm_service):
    user_message = "What's your favorite color?"
    context = {"previous_topic": "colors"}
    style = {"tone": "friendly"}
    
    prompt = llm_service.format_prompt(user_message, context, style)
    
    assert "Context: {'previous_topic': 'colors'}" in prompt
    assert "Style: {'tone': 'friendly'}" in prompt
    assert f"User: {user_message}" in prompt
    assert "Assistant:" in prompt

@pytest.mark.asyncio
async def test_generate_response_error_handling(llm_service):
    test_prompt = "Hello"
    error_message = "API Error"
    
    llm_service.model.generate_content_async.side_effect = Exception(error_message)
    
    with pytest.raises(Exception) as exc_info:
        await llm_service.generate_response(test_prompt)
    
    assert str(exc_info.value) == f"Error generating response: {error_message}" 