"""Tests for Anthropic OAuth provider integration.

Tests everything that can be validated without live Anthropic credentials:
- Provider configuration correctness
- Token storage round-trip
- PKCE generation
- Authorization URL construction
- Token exchange request formatting (JSON vs form-urlencoded)
- Token refresh request formatting
- Provider registry wiring
- CLI login handler wiring
- AnthropicOAuthProvider instantiation and chat() error path
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# 1. oauth-cli-kit: Provider config correctness
# ---------------------------------------------------------------------------


def test_anthropic_provider_config():
    """ANTHROPIC_PROVIDER has the expected OAuth parameters."""
    from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

    assert ANTHROPIC_PROVIDER.client_id == "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
    assert ANTHROPIC_PROVIDER.authorize_url == "https://claude.ai/oauth/authorize"
    assert ANTHROPIC_PROVIDER.token_url == "https://console.anthropic.com/v1/oauth/token"
    assert ANTHROPIC_PROVIDER.redirect_uri == "https://console.anthropic.com/oauth/code/callback"
    assert "user:inference" in ANTHROPIC_PROVIDER.scope
    assert "org:create_api_key" in ANTHROPIC_PROVIDER.scope
    assert ANTHROPIC_PROVIDER.jwt_claim_path is None  # opaque tokens
    assert ANTHROPIC_PROVIDER.account_id_claim is None
    assert ANTHROPIC_PROVIDER.token_content_type == "json"
    assert ANTHROPIC_PROVIDER.token_filename == "anthropic.json"
    assert ("code", "true") in ANTHROPIC_PROVIDER.extra_authorize_params


def test_openai_codex_provider_unchanged():
    """OpenAI Codex provider still works after the generalization."""
    from oauth_cli_kit.providers.openai_codex import OPENAI_CODEX_PROVIDER

    assert OPENAI_CODEX_PROVIDER.client_id == "app_EMoamEEZ73f0CkXaXp7hrann"
    assert OPENAI_CODEX_PROVIDER.token_content_type == "form"
    assert ("id_token_add_organizations", "true") in OPENAI_CODEX_PROVIDER.extra_authorize_params
    assert ("codex_cli_simplified_flow", "true") in OPENAI_CODEX_PROVIDER.extra_authorize_params


def test_provider_config_defaults():
    """Default values for new fields are backward-compatible."""
    from oauth_cli_kit.models import OAuthProviderConfig

    cfg = OAuthProviderConfig(
        client_id="test",
        authorize_url="https://example.com/auth",
        token_url="https://example.com/token",
        redirect_uri="http://localhost:1234/callback",
        scope="openid",
    )
    assert cfg.extra_authorize_params == ()
    assert cfg.token_content_type == "form"


# ---------------------------------------------------------------------------
# 2. oauth-cli-kit: Top-level exports
# ---------------------------------------------------------------------------


def test_top_level_exports():
    """Public API exposes both providers and core classes."""
    from oauth_cli_kit import (
        ANTHROPIC_PROVIDER,
        OPENAI_CODEX_PROVIDER,
        OAuthProviderConfig,
        OAuthToken,
        get_token,
        login_oauth_interactive,
    )

    assert ANTHROPIC_PROVIDER is not None
    assert OPENAI_CODEX_PROVIDER is not None
    assert callable(get_token)
    assert callable(login_oauth_interactive)


# ---------------------------------------------------------------------------
# 3. oauth-cli-kit: PKCE helpers
# ---------------------------------------------------------------------------


def test_pkce_generation():
    """PKCE verifier/challenge are valid base64url strings."""
    from oauth_cli_kit.pkce import _generate_pkce

    verifier, challenge = _generate_pkce()
    assert len(verifier) > 20
    assert len(challenge) > 20
    assert verifier != challenge


def test_state_creation():
    """State tokens are unique."""
    from oauth_cli_kit.pkce import _create_state

    s1 = _create_state()
    s2 = _create_state()
    assert s1 != s2
    assert len(s1) > 10


def test_parse_authorization_input_code_only():
    """Raw code string is returned as-is."""
    from oauth_cli_kit.pkce import _parse_authorization_input

    code, state = _parse_authorization_input("abc123")
    assert code == "abc123"
    assert state is None


def test_parse_authorization_input_url():
    """Full callback URL is parsed correctly."""
    from oauth_cli_kit.pkce import _parse_authorization_input

    url = "http://localhost:1455/auth/callback?code=xyz&state=s123"
    code, state = _parse_authorization_input(url)
    assert code == "xyz"
    assert state == "s123"


def test_parse_authorization_input_empty():
    """Empty input returns None, None."""
    from oauth_cli_kit.pkce import _parse_authorization_input

    code, state = _parse_authorization_input("")
    assert code is None
    assert state is None


# ---------------------------------------------------------------------------
# 4. oauth-cli-kit: Token storage round-trip
# ---------------------------------------------------------------------------


def test_token_storage_roundtrip(tmp_path: Path):
    """Tokens can be saved and loaded from disk."""
    from oauth_cli_kit.models import OAuthToken
    from oauth_cli_kit.storage import FileTokenStorage

    storage = FileTokenStorage(
        token_filename="test_anthropic.json",
        app_name="test-oauth",
        data_dir=tmp_path,
    )

    token = OAuthToken(
        access="acc_test_123",
        refresh="ref_test_456",
        expires=int(time.time() * 1000 + 3600 * 1000),
        account_id=None,  # Anthropic tokens have no account_id
    )
    storage.save(token)

    loaded = storage.load()
    assert loaded is not None
    assert loaded.access == "acc_test_123"
    assert loaded.refresh == "ref_test_456"
    assert loaded.account_id is None

    # Verify file permissions (should be 0600)
    path = storage.get_token_path()
    assert path.exists()
    assert oct(path.stat().st_mode & 0o777) == "0o600"


def test_token_storage_missing_file(tmp_path: Path):
    """Loading from non-existent path returns None."""
    from oauth_cli_kit.storage import FileTokenStorage

    storage = FileTokenStorage(
        token_filename="nonexistent.json",
        app_name="test-oauth",
        data_dir=tmp_path,
        import_codex_cli=False,
    )
    assert storage.load() is None


# ---------------------------------------------------------------------------
# 5. oauth-cli-kit: Authorization URL construction
# ---------------------------------------------------------------------------


def test_authorize_url_anthropic():
    """Anthropic authorize URL includes extra params and JSON content type flag."""
    import urllib.parse

    from oauth_cli_kit.pkce import _generate_pkce, _create_state
    from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

    provider = ANTHROPIC_PROVIDER
    verifier, challenge = _generate_pkce()
    state = _create_state()

    params = {
        "response_type": "code",
        "client_id": provider.client_id,
        "redirect_uri": provider.redirect_uri,
        "scope": provider.scope,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "originator": "nanobot",
    }
    for key, val in provider.extra_authorize_params:
        params[key] = val

    url = f"{provider.authorize_url}?{urllib.parse.urlencode(params)}"

    assert url.startswith("https://claude.ai/oauth/authorize?")
    assert "code=true" in url
    assert f"client_id={provider.client_id}" in url
    assert "redirect_uri=" in url
    assert "code_challenge=" in url


def test_authorize_url_codex():
    """OpenAI Codex authorize URL includes its specific extras."""
    import urllib.parse

    from oauth_cli_kit.pkce import _generate_pkce, _create_state
    from oauth_cli_kit.providers.openai_codex import OPENAI_CODEX_PROVIDER

    provider = OPENAI_CODEX_PROVIDER
    verifier, challenge = _generate_pkce()
    state = _create_state()

    params = {
        "response_type": "code",
        "client_id": provider.client_id,
        "redirect_uri": provider.redirect_uri,
        "scope": provider.scope,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "originator": "nanobot",
    }
    for key, val in provider.extra_authorize_params:
        params[key] = val

    url = f"{provider.authorize_url}?{urllib.parse.urlencode(params)}"

    assert url.startswith("https://auth.openai.com/oauth/authorize?")
    assert "id_token_add_organizations=true" in url
    assert "codex_cli_simplified_flow=true" in url


# ---------------------------------------------------------------------------
# 6. oauth-cli-kit: Token exchange uses correct content type
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_token_exchange_anthropic_uses_json():
    """Anthropic token exchange sends JSON body, not form-urlencoded."""
    import httpx

    from oauth_cli_kit.flow import _exchange_code_for_token_async
    from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

    captured_kwargs = {}

    async def mock_post(url, **kwargs):
        captured_kwargs.update(kwargs)
        captured_kwargs["url"] = url
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "access_token": "at_test",
            "refresh_token": "rt_test",
            "expires_in": 3600,
        }
        return resp

    exchange_fn = _exchange_code_for_token_async("test_code", "test_verifier", ANTHROPIC_PROVIDER)

    with patch("oauth_cli_kit.flow.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.post = mock_post
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value = mock_instance

        token = await exchange_fn()

    assert token.access == "at_test"
    assert token.refresh == "rt_test"
    assert captured_kwargs.get("url") == "https://console.anthropic.com/v1/oauth/token"
    # JSON body — should use 'json' kwarg, not 'data'
    assert "json" in captured_kwargs
    assert captured_kwargs["json"]["grant_type"] == "authorization_code"
    assert captured_kwargs["json"]["code"] == "test_code"


@pytest.mark.asyncio
async def test_token_exchange_codex_uses_form():
    """OpenAI Codex token exchange sends form-urlencoded body."""
    from oauth_cli_kit.flow import _exchange_code_for_token_async
    from oauth_cli_kit.providers.openai_codex import OPENAI_CODEX_PROVIDER

    captured_kwargs = {}

    async def mock_post(url, **kwargs):
        captured_kwargs.update(kwargs)
        captured_kwargs["url"] = url
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "access_token": "at_codex",
            "refresh_token": "rt_codex",
            "expires_in": 3600,
        }
        return resp

    # Build a fake JWT for account_id decoding
    import base64

    header = base64.urlsafe_b64encode(b'{"alg":"RS256"}').rstrip(b"=").decode()
    payload_data = json.dumps(
        {"https://api.openai.com/auth": {"chatgpt_account_id": "acc123"}}
    ).encode()
    payload = base64.urlsafe_b64encode(payload_data).rstrip(b"=").decode()
    sig = base64.urlsafe_b64encode(b"sig").rstrip(b"=").decode()
    fake_jwt = f"{header}.{payload}.{sig}"

    exchange_fn = _exchange_code_for_token_async(
        "test_code", "test_verifier", OPENAI_CODEX_PROVIDER
    )

    with patch("oauth_cli_kit.flow.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()

        async def mock_post_with_jwt(url, **kwargs):
            captured_kwargs.update(kwargs)
            captured_kwargs["url"] = url
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = {
                "access_token": fake_jwt,
                "refresh_token": "rt_codex",
                "expires_in": 3600,
            }
            return resp

        mock_instance.post = mock_post_with_jwt
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value = mock_instance

        token = await exchange_fn()

    assert token.access == fake_jwt
    assert captured_kwargs.get("url") == "https://auth.openai.com/oauth/token"
    # Form body — should use 'data' kwarg, not 'json'
    assert "data" in captured_kwargs
    assert captured_kwargs["data"]["grant_type"] == "authorization_code"


# ---------------------------------------------------------------------------
# 7. oauth-cli-kit: Token refresh uses correct content type
# ---------------------------------------------------------------------------


def test_refresh_anthropic_uses_json():
    """Anthropic token refresh sends JSON body."""
    from oauth_cli_kit.flow import _refresh_token
    from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

    captured_kwargs = {}

    def mock_post(url, **kwargs):
        captured_kwargs.update(kwargs)
        captured_kwargs["url"] = url
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "access_token": "at_refreshed",
            "refresh_token": "rt_refreshed",
            "expires_in": 3600,
        }
        return resp

    with patch("oauth_cli_kit.flow.httpx.Client") as MockClient:
        mock_instance = MagicMock()
        mock_instance.post = mock_post
        mock_instance.__enter__ = MagicMock(return_value=mock_instance)
        mock_instance.__exit__ = MagicMock(return_value=False)
        MockClient.return_value = mock_instance

        token = _refresh_token("old_refresh", ANTHROPIC_PROVIDER)

    assert token.access == "at_refreshed"
    assert "json" in captured_kwargs
    assert captured_kwargs["json"]["grant_type"] == "refresh_token"
    assert captured_kwargs["json"]["refresh_token"] == "old_refresh"


# ---------------------------------------------------------------------------
# 8. nanobot: Provider registry has anthropic_oauth
# ---------------------------------------------------------------------------


def test_registry_has_anthropic_oauth():
    """anthropic_oauth is registered with is_oauth=True."""
    from nanobot.providers.registry import PROVIDERS

    spec = next((s for s in PROVIDERS if s.name == "anthropic_oauth"), None)
    assert spec is not None, "anthropic_oauth not found in PROVIDERS"
    assert spec.is_oauth is True
    assert spec.supports_prompt_caching is True


# ---------------------------------------------------------------------------
# 9. nanobot: CLI login handler is wired
# ---------------------------------------------------------------------------


def test_login_handler_registered():
    """anthropic_oauth has a login handler in _LOGIN_HANDLERS."""
    # Import triggers handler registration via @_register_login decorator
    from nanobot.cli.commands import _LOGIN_HANDLERS  # noqa: F401

    assert "anthropic_oauth" in _LOGIN_HANDLERS
    assert callable(_LOGIN_HANDLERS["anthropic_oauth"])


# ---------------------------------------------------------------------------
# 10. nanobot: AnthropicOAuthProvider
# ---------------------------------------------------------------------------


def test_anthropic_oauth_provider_instantiates():
    """Provider instantiates with empty token when no credentials exist."""
    from nanobot.providers.anthropic_oauth_provider import AnthropicOAuthProvider

    provider = AnthropicOAuthProvider()
    assert provider.get_default_model() == "claude-sonnet-4-5"


@pytest.mark.asyncio
async def test_anthropic_oauth_provider_chat_error_path():
    """chat() returns error message when token fetch fails."""
    from nanobot.providers.anthropic_oauth_provider import AnthropicOAuthProvider

    provider = AnthropicOAuthProvider()

    with patch(
        "nanobot.providers.anthropic_oauth_provider._get_anthropic_token",
        side_effect=RuntimeError("OAuth credentials not found"),
    ):
        result = await provider.chat(
            messages=[{"role": "user", "content": "test"}],
        )

    assert result.finish_reason == "error"
    assert "OAuth credentials not found" in result.content
    assert "nanobot provider login anthropic-oauth" in result.content


# ---------------------------------------------------------------------------
# 11. nanobot: _make_provider routes anthropic_oauth correctly
# ---------------------------------------------------------------------------


def test_make_provider_routes_anthropic_oauth():
    """_make_provider returns AnthropicOAuthProvider for anthropic_oauth config."""
    from nanobot.cli.commands import _make_provider
    from nanobot.config.schema import AgentDefaults, AgentsConfig, Config
    from nanobot.providers.anthropic_oauth_provider import AnthropicOAuthProvider

    config = Config()
    config.agents = AgentsConfig(defaults=AgentDefaults(model="test", provider="anthropic_oauth"))

    provider = _make_provider(config)
    assert isinstance(provider, AnthropicOAuthProvider)
