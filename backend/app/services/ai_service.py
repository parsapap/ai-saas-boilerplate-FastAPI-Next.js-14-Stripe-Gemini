import google.generativeai as genai
from typing import List, AsyncGenerator
import time
from app.core.config import settings
from app.schemas.ai import Message
from app.core.ai_config import AI_MODELS

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class AIService:
    """Service for AI model interactions"""
    
    @staticmethod
    async def chat_completion(
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> dict:
        """
        Get chat completion from AI model
        
        Returns: {
            "message": str,
            "usage": {"input_tokens": int, "output_tokens": int, "total_tokens": int},
            "finish_reason": str,
            "duration_ms": int
        }
        """
        start_time = time.time()
        
        if model.startswith("gemini"):
            result = await AIService._gemini_completion(messages, model, temperature, max_tokens)
        elif model.startswith("claude"):
            result = await AIService._claude_completion(messages, model, temperature, max_tokens)
        elif model.startswith("gpt"):
            result = await AIService._openai_completion(messages, model, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        duration_ms = int((time.time() - start_time) * 1000)
        result["duration_ms"] = duration_ms
        
        return result
    
    @staticmethod
    async def chat_completion_stream(
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion"""
        if model.startswith("gemini"):
            async for chunk in AIService._gemini_stream(messages, model, temperature, max_tokens):
                yield chunk
        else:
            # For now, only Gemini supports streaming
            result = await AIService.chat_completion(messages, model, temperature, max_tokens)
            yield result["message"]
    
    @staticmethod
    async def _gemini_completion(
        messages: List[Message],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> dict:
        """Gemini completion"""
        # Map model name to actual Gemini API model names
        model_map = {
            "gemini-1.5-flash": "gemini-1.5-flash-latest",
            "gemini-1.5-pro": "gemini-1.5-pro-latest",
            "gemini-2.0-flash": "gemini-2.0-flash-exp",
        }
        model_name = model_map.get(model, "gemini-2.0-flash-exp")
        
        # Initialize model
        gemini_model = genai.GenerativeModel(model_name)
        
        # Convert messages to Gemini format
        chat_history = []
        user_message = ""
        
        for msg in messages:
            if msg.role == "system":
                # Gemini doesn't have system role, prepend to first user message
                continue
            elif msg.role == "user":
                user_message = msg.content
            elif msg.role == "assistant":
                chat_history.append({
                    "role": "user",
                    "parts": [user_message]
                })
                chat_history.append({
                    "role": "model",
                    "parts": [msg.content]
                })
        
        # Start chat
        chat = gemini_model.start_chat(history=chat_history)
        
        # Generate response
        response = chat.send_message(
            user_message,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        # Extract usage
        usage = {
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count
        }
        
        return {
            "message": response.text,
            "usage": usage,
            "finish_reason": "stop"
        }
    
    @staticmethod
    async def _gemini_stream(
        messages: List[Message],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:
        """Gemini streaming"""
        # Map model name to actual Gemini API model names
        model_map = {
            "gemini-1.5-flash": "gemini-1.5-flash-latest",
            "gemini-1.5-pro": "gemini-1.5-pro-latest",
            "gemini-2.0-flash": "gemini-2.0-flash-exp",
        }
        model_name = model_map.get(model, "gemini-2.0-flash-exp")
        gemini_model = genai.GenerativeModel(model_name)
        
        # Get last user message
        user_message = messages[-1].content
        
        # Stream response
        response = gemini_model.generate_content(
            user_message,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            ),
            stream=True
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    
    @staticmethod
    async def _claude_completion(messages, model, temperature, max_tokens) -> dict:
        """Claude completion (placeholder)"""
        # TODO: Implement Claude API
        return {
            "message": "Claude integration coming soon!",
            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            "finish_reason": "stop"
        }
    
    @staticmethod
    async def _openai_completion(messages, model, temperature, max_tokens) -> dict:
        """OpenAI completion (placeholder)"""
        # TODO: Implement OpenAI API
        return {
            "message": "OpenAI integration coming soon!",
            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            "finish_reason": "stop"
        }
