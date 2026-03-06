"""Phase C-5 test: spawn 4 parallel writer subagents and verify output."""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT = Path.home() / "Dropbox/AgentWorkspace/PaperAutoGen/r01-older-adults-mci-home-ai"
WORKSPACE = Path.home() / ".nanobot/workspace"
SYSTEM_DIR = Path.home() / "Dropbox/AgentWorkspace/PaperAutoGen/_system"
EXAMPLES_DIR = Path.home() / "Dropbox/AgentWorkspace/PriorNIHR01Examples"

# Skill paths (built-in)
SKILLS_DIR = Path(__file__).parent.parent / "nanobot" / "skills"


def build_writer_prompt(skill_name: str, sections: dict[str, dict]) -> str:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    section_specs = "\n".join(
        f"  - {name}: {info['word_target']} words → {PROJECT / info['output']}"
        for name, info in sections.items()
    )
    return f"""You are a writing subagent. Read the {skill_name} skill at {skill_path} and follow its instructions.

PROJECT: {PROJECT}
SECTIONS TO WRITE:
{section_specs}

REQUIRED INPUTS (read these before writing):
- Project config: {PROJECT}/project.yaml
- Proposal outline: {PROJECT}/docs/outline.md (find your section specs here)
- Literature: {PROJECT}/literature/refs.json and {PROJECT}/literature/gaps.md
- Selected idea: {PROJECT}/ideas/ideas.json
- Style references: {EXAMPLES_DIR}/ (read 1-2 for voice calibration)
- System style guide: {SYSTEM_DIR}/style_guide.md
- Section specs: {SYSTEM_DIR}/r01_section_specs.md

INSTRUCTIONS:
1. Read the skill file first for your role and quality standards.
2. Read outline.md and locate YOUR assigned section(s) — use the heading structure and word targets there.
3. Read refs.json and gaps.md to incorporate citations and address gaps.
4. Read 1-2 prior examples from PriorNIHR01Examples/ for NIH voice calibration.
5. Write each section to its output file. Use markdown with proper heading hierarchy.
6. Each section MUST meet its word target (±10%).
7. Cite references using [AuthorYear] format matching refs.json entries.
8. Do NOT modify state.json — the orchestrator handles tracking."""


BATCHES = [
    {
        "label": "integrator-framing",
        "skill": "r01-writer-integrator",
        "sections": {
            "specific_aims": {"word_target": 500, "output": "docs/drafts/specific_aims_v1.md"},
            "significance": {"word_target": 1500, "output": "docs/drafts/significance_v1.md"},
            "innovation": {"word_target": 1000, "output": "docs/drafts/innovation_v1.md"},
        },
    },
    {
        "label": "writer-hci-aim1",
        "skill": "r01-writer-hci",
        "sections": {
            "approach_aim1": {"word_target": 1500, "output": "docs/drafts/approach_aim1_v1.md"},
        },
    },
    {
        "label": "writer-ai-aim2",
        "skill": "r01-writer-ai",
        "sections": {
            "approach_aim2": {"word_target": 1500, "output": "docs/drafts/approach_aim2_v1.md"},
        },
    },
    {
        "label": "writer-healthcare-aim3",
        "skill": "r01-writer-healthcare",
        "sections": {
            "approach_aim3": {"word_target": 1500, "output": "docs/drafts/approach_aim3_v1.md"},
        },
    },
]


async def run_test():
    from nanobot.agent.subagent import SubagentManager
    from nanobot.bus.queue import MessageBus
    from nanobot.config.loader import load_config

    config = load_config()
    model = config.agents.defaults.model

    # Create provider (same as CLI)
    from nanobot.providers.litellm_provider import LiteLLMProvider

    provider_name = config.get_provider_name(model)
    p = config.get_provider(model)
    provider = LiteLLMProvider(
        api_key=p.api_key if p else None,
        api_base=config.get_api_base(model),
        default_model=model,
        provider_name=provider_name,
    )

    bus = MessageBus()
    mgr = SubagentManager(
        provider=provider,
        workspace=WORKSPACE,
        bus=bus,
        model=model,
        temperature=0.7,
        max_tokens=16384,
    )

    print(f"Provider: {provider_name}, Model: {model}")
    print(f"Project: {PROJECT}")
    print(f"Spawning {len(BATCHES)} writer batches...\n")

    start = time.time()
    results = []

    for batch in BATCHES:
        prompt = build_writer_prompt(batch["skill"], batch["sections"])
        result_msg = await mgr.spawn(
            task=prompt,
            label=batch["label"],
            max_iterations=30,
        )
        print(f"  [{batch['label']}] {result_msg}")
        results.append(batch)

    print(f"\nAll {len(BATCHES)} batches spawned. Waiting for completion...")
    print("(Subagents run concurrently — watching for output files)\n")

    expected_files = []
    for batch in BATCHES:
        for info in batch["sections"].values():
            expected_files.append(PROJECT / info["output"])

    # Poll for completion (check file existence + subagent count)
    max_wait = 600  # 10 minutes
    poll_interval = 10
    elapsed = 0

    while elapsed < max_wait:
        await asyncio.sleep(poll_interval)
        elapsed = int(time.time() - start)
        running = mgr.get_running_count()
        found = [f for f in expected_files if f.exists()]
        print(
            f"  [{elapsed:3d}s] running={running}, files={len(found)}/{len(expected_files)}: {[f.name for f in found]}"
        )

        if running == 0:
            print("\nAll subagents finished.")
            break

        # Drain bus messages (prevent queue buildup)
        while not bus.inbound.empty():
            msg = await bus.consume_inbound()
            label = msg.content[:80].replace("\n", " ")
            print(f"  [BUS] {label}...")
    else:
        print(f"\nTimeout after {max_wait}s. {mgr.get_running_count()} subagents still running.")

    # Final check
    print("\n=== RESULTS ===")
    total_words = 0
    for f in expected_files:
        if f.exists():
            content = f.read_text()
            wc = len(content.split())
            total_words += wc
            print(f"  ✓ {f.name}: {wc} words, {len(content)} chars")
        else:
            print(f"  ✗ {f.name}: MISSING")

    print(
        f"\nTotal: {len([f for f in expected_files if f.exists()])}/{len(expected_files)} files, {total_words} words"
    )
    print(f"Elapsed: {int(time.time() - start)}s")


if __name__ == "__main__":
    asyncio.run(run_test())
