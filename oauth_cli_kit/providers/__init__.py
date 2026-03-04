"""OAuth Provider configurations.

Design goals:
1) Unified management of OAuth configs for multiple CLIs (Codex, Claude, etc.)
   as a providers sub-package.
2) Preserve existing public API (e.g. oauth_cli_kit.constants.OPENAI_CODEX_PROVIDER).
3) Adding a new provider only requires a new module in this directory plus an
   export here.
"""

from oauth_cli_kit.providers.openai_codex import OPENAI_CODEX_PROVIDER
from oauth_cli_kit.providers.anthropic import ANTHROPIC_PROVIDER

__all__ = [
    "OPENAI_CODEX_PROVIDER",
    "ANTHROPIC_PROVIDER",
]
