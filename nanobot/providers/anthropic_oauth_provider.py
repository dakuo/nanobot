"""Anthropic OAuth provider — Claude Pro/Max subscription login.

Uses the oauth-cli-kit ANTHROPIC_PROVIDER config to perform browser-based
OAuth login with Anthropic.  At runtime the stored OAuth token is read
on every request (auto-refreshed by oauth-cli-kit when it expires) and
passed to LiteLLM which sends it as ``Authorization: Bearer`` with the
``anthropic-beta: oauth-2025-04-20`` header.

No separate API key is needed — the user's Claude Pro/Max subscription
is billed instead.
"""

from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger

from nanobot.providers.base import LLMResponse
from nanobot.providers.litellm_provider import LiteLLMProvider


def _get_anthropic_token() -> str:
    """Return the current Anthropic OAuth access token via oauth-cli-kit."""
    from oauth_cli_kit import get_token
    from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

    token = get_token(provider=ANTHROPIC_PROVIDER)
    return token.access


class AnthropicOAuthProvider(LiteLLMProvider):
    """LiteLLM-based provider that authenticates via Anthropic OAuth tokens.

    The token is re-read on every ``chat()`` call so that background
    refreshes performed by oauth-cli-kit are picked up automatically.
    """

    def __init__(self, default_model: str = "claude-sonnet-4-5"):
        # Attempt to read an existing token; fall back to empty string
        # (the login command should be run first).
        try:
            token = _get_anthropic_token()
        except Exception:
            token = ""
        super().__init__(
            api_key=token,
            default_model=default_model,
            provider_name="anthropic",
        )

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        reasoning_effort: str | None = None,
    ) -> LLMResponse:
        # Re-read token each call — oauth-cli-kit may have refreshed it.
        try:
            self.api_key = await asyncio.to_thread(_get_anthropic_token)
        except Exception as e:
            logger.warning(f"Failed to read Anthropic OAuth token: {e}")
            return LLMResponse(
                content=(
                    f"Anthropic OAuth error: {e}\n\n"
                    "Please run `nanobot provider login anthropic-oauth` to authenticate."
                ),
                finish_reason="error",
            )
        return await super().chat(
            messages,
            tools,
            model,
            max_tokens,
            temperature,
            reasoning_effort,
        )

    def get_default_model(self) -> str:
        return self.default_model
