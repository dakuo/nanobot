"""Anthropic (Claude Pro/Max) OAuth Provider configuration."""

from __future__ import annotations

from oauth_cli_kit.models import OAuthProviderConfig


# Anthropic OAuth — uses claude.ai authorize endpoint, console.anthropic.com
# for token exchange. The redirect URI shows a code on the page that the user
# copies back to the CLI (no localhost callback).
ANTHROPIC_PROVIDER = OAuthProviderConfig(
    client_id="9d1c250a-e61b-44d9-88ed-5944d1962f5e",
    authorize_url="https://claude.ai/oauth/authorize",
    token_url="https://console.anthropic.com/v1/oauth/token",
    redirect_uri="https://console.anthropic.com/oauth/code/callback",
    scope="org:create_api_key user:profile user:inference",
    jwt_claim_path=None,  # Anthropic tokens are opaque, not JWT
    account_id_claim=None,
    default_originator="nanobot",
    token_filename="anthropic.json",
    extra_authorize_params=(("code", "true"),),
    token_content_type="json",
)
