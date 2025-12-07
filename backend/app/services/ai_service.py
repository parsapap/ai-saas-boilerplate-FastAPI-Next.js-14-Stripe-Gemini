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
        """Gemini completion via OpenRouter"""
        import httpx
        import json
        
        # Map model name to OpenRouter free models
        model_map = {
            "gemini-1.5-flash": "google/gemma-3n-e4b-it:free",
            "gemini-1.5-pro": "google/gemma-3n-e4b-it:free",
            "gemini-2.0-flash": "google/gemma-3n-e4b-it:free",
        }
        openrouter_model = model_map.get(model, "google/gemma-3n-e4b-it:free")
        
        # Convert messages to OpenRouter format
        openrouter_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Use OpenRouter API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": openrouter_model,
                    "messages": openrouter_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=60.0,
            )
            
            result = response.json()
            
            # Check for API errors
            if response.status_code != 200:
                error_msg = result.get("error", {}).get("message", str(result))
                if response.status_code == 429:
                    raise Exception("Rate limit exceeded. The AI service has reached its daily limit. Please try again later or contact support.")
                raise Exception(f"OpenRouter API error ({response.status_code}): {error_msg}")
            
            if "choices" not in result or len(result["choices"]) == 0:
                raise Exception(f"Invalid API response: {json.dumps(result)}")
            
            return {
                "message": result["choices"][0]["message"]["content"],
                "usage": {
                    "input_tokens": result.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": result.get("usage", {}).get("completion_tokens", 0),
                    "total_tokens": result.get("usage", {}).get("total_tokens", 0),
                },
                "finish_reason": result["choices"][0].get("finish_reason", "stop")
            }
    
    @staticmethod
    async def _gemini_stream(
        messages: List[Message],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:
        """Gemini streaming via OpenRouter"""
        import httpx
        
        # Map model name to OpenRouter free models
        model_map = {
            "gemini-1.5-flash": "google/gemma-3n-e4b-it:free",
            "gemini-1.5-pro": "google/gemma-3n-e4b-it:free",
            "gemini-2.0-flash": "google/gemma-3n-e4b-it:free",
        }
        openrouter_model = model_map.get(model, "google/gemma-3n-e4b-it:free")
        
        # Convert messages to OpenRouter format
        openrouter_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Use OpenRouter API
        import json
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Using OpenRouter model: {openrouter_model}")
        
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": openrouter_model,
                    "messages": openrouter_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                },
                timeout=60.0,
            ) as response:
                logger.info(f"OpenRouter streaming response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_data = json.loads(error_text.decode())
                    error_msg = error_data.get("error", {}).get("message", "Unknown error")
                    logger.error(f"OpenRouter error ({response.status_code}): {error_msg}")
                    
                    # Return user-friendly error message
                    if response.status_code == 429:
                        yield "⚠️ Rate limit exceeded. The AI service has reached its daily limit. Please try again later or contact support."
                    else:
                        yield f"⚠️ AI service error: {error_msg}"
                    return
                
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    
                    logger.debug(f"Received line: {line[:200]}")
                        
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data == "[DONE]":
                            logger.info("Received [DONE] signal")
                            break
                        
                        try:
                            chunk_data = json.loads(data)
                            logger.debug(f"Parsed chunk: {chunk_data}")
                            if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                delta = chunk_data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    logger.debug(f"Yielding content: {content}")
                                    yield content
                            else:
                                logger.warning(f"No choices in chunk: {chunk_data}")
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse SSE data: {data[:100]}")
                        except Exception as e:
                            logger.error(f"Error processing chunk: {e}")
    
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
