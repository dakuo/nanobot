from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from loguru import logger


class Mem0Store:
    def __init__(self, ollama_url: str, embedding_model: str, llm_model: str):
        self._memory: Any | None = None
        self._initialize(ollama_url=ollama_url, embedding_model=embedding_model, llm_model=llm_model)

    def _initialize(self, *, ollama_url: str, embedding_model: str, llm_model: str) -> None:
        try:
            memory_module = importlib.import_module("mem0")
            Memory = getattr(memory_module, "Memory")
        except ImportError:
            logger.warning("mem0 is enabled but mem0ai is not installed; semantic memory disabled")
            return
        except Exception as exc:
            logger.warning("mem0 is enabled but failed to import: {}", exc)
            return

        data_dir = Path.home() / ".nanobot"
        config = {
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": embedding_model,
                    "ollama_base_url": ollama_url,
                },
            },
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": llm_model,
                    "ollama_base_url": ollama_url,
                    "temperature": 0.0,
                },
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "nanobot_memories",
                    "path": str(data_dir / "mem0_store"),
                },
            },
            "version": "v1.1",
        }

        try:
            if hasattr(Memory, "from_config"):
                self._memory = Memory.from_config(config)
            else:
                self._memory = Memory(config=config)
        except Exception as exc:
            logger.warning("Failed to initialize mem0 semantic memory: {}", exc)
            self._memory = None

    @staticmethod
    def _format_memories(results: Any) -> str:
        if not results:
            return ""

        if isinstance(results, dict):
            if isinstance(results.get("results"), list):
                items = results["results"]
            elif isinstance(results.get("memories"), list):
                items = results["memories"]
            else:
                items = [results]
        elif isinstance(results, list):
            items = results
        else:
            items = [results]

        lines: list[str] = []
        for item in items:
            if isinstance(item, str):
                text = item.strip()
            elif isinstance(item, dict):
                text = str(
                    item.get("memory")
                    or item.get("text")
                    or item.get("content")
                    or item.get("value")
                    or ""
                ).strip()
            else:
                text = str(item).strip()

            if text:
                lines.append(f"- {text}")

        return "\n".join(lines)

    def add(self, text: str, user_id: str = "default") -> None:
        if not self._memory or not text.strip():
            return
        try:
            self._memory.add(text, user_id=user_id)
        except Exception as exc:
            logger.warning("mem0 add failed: {}", exc)

    def search(self, query: str, user_id: str = "default", limit: int = 5) -> str:
        if not self._memory or not query.strip():
            return ""
        try:
            results = self._memory.search(query, user_id=user_id, limit=limit)
            return self._format_memories(results)
        except Exception as exc:
            logger.warning("mem0 search failed: {}", exc)
            return ""

    def get_all(self, user_id: str = "default") -> str:
        if not self._memory:
            return ""
        try:
            results = self._memory.get_all(user_id=user_id)
            return self._format_memories(results)
        except Exception as exc:
            logger.warning("mem0 get_all failed: {}", exc)
            return ""
