"""
AI Client - Unified interface for Claude/OpenAI
"""

from typing import Optional, Dict, Any
from loguru import logger
from config import settings


class AIClient:
    """Unified AI client supporting both Anthropic and OpenAI"""

    def __init__(self):
        self.provider = settings.ai_provider
        self.model = settings.ai_model
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                client = Anthropic(api_key=settings.anthropic_api_key)
                logger.info(f"Initialized Anthropic client with model: {self.model}")
                return client
            except ImportError:
                logger.error("Anthropic package not installed. Run: pip install anthropic")
                raise
        elif self.provider == "openai":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.openai_api_key)
                logger.info(f"Initialized OpenAI client with model: {self.model}")
                return client
            except ImportError:
                logger.error("OpenAI package not installed. Run: pip install openai")
                raise
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using the configured AI provider

        Args:
            prompt: The user prompt/input
            system_prompt: Optional system prompt to set context
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0-1.0)

        Returns:
            Generated text response
        """
        try:
            if self.provider == "anthropic":
                return self._generate_anthropic(prompt, system_prompt, max_tokens, temperature)
            elif self.provider == "openai":
                return self._generate_openai(prompt, system_prompt, max_tokens, temperature)
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise

    def _generate_anthropic(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int, temperature: float
    ) -> str:
        """Generate using Anthropic Claude"""
        messages = [{"role": "user", "content": prompt}]

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def _generate_openai(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int, temperature: float
    ) -> str:
        """Generate using OpenAI GPT"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content

    def generate_with_context(
        self,
        prompt_template: str,
        context: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate text with a template and context variables

        Args:
            prompt_template: Template string with {variables}
            context: Dictionary of variables to fill in template
            system_prompt: Optional system prompt
            **kwargs: Additional arguments for generate()

        Returns:
            Generated text response
        """
        # Fill in the template with context
        prompt = prompt_template.format(**context)

        logger.debug(f"Generated prompt with context: {len(prompt)} chars")

        return self.generate(prompt, system_prompt, **kwargs)


# Global AI client instance
ai_client = AIClient()


if __name__ == "__main__":
    # Test the AI client
    print("Testing AI Client...")
    print("=" * 50)

    test_prompt = "Write a brief daily plan for a product manager with 3 priorities."
    system_prompt = "You are a helpful assistant for product managers."

    try:
        response = ai_client.generate(test_prompt, system_prompt, max_tokens=500)
        print("Response:")
        print(response)
        print("\n" + "=" * 50)
        print("✅ AI Client test successful")
    except Exception as e:
        print(f"❌ AI Client test failed: {e}")
