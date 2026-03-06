"""Phase C-5 Batch E: integrator assembly — write remaining sections + merge."""

import asyncio
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT = Path.home() / "Dropbox/AgentWorkspace/PaperAutoGen/r01-older-adults-mci-home-ai"
WORKSPACE = Path.home() / ".nanobot/workspace"
SYSTEM_DIR = Path.home() / "Dropbox/AgentWorkspace/PaperAutoGen/_system"
EXAMPLES_DIR = Path.home() / "Dropbox/AgentWorkspace/PriorNIHR01Examples"
SKILLS_DIR = Path(__file__).parent.parent / "nanobot" / "skills"

INTEGRATOR_SKILL = SKILLS_DIR / "r01-writer-integrator" / "SKILL.md"

ASSEMBLY_PROMPT = f"""You are the integration writer. Read the r01-writer-integrator skill at {INTEGRATOR_SKILL} and follow its instructions.

PROJECT: {PROJECT}

PHASE 1 — Write remaining sections:
- approach_timeline: 300 words → {PROJECT}/docs/drafts/approach_timeline_v1.md
- approach_crosscutting: 300 words → {PROJECT}/docs/drafts/approach_crosscutting_v1.md
- project_narrative: 1 sentence → {PROJECT}/docs/drafts/project_narrative_v1.md
- project_summary: 30 lines → {PROJECT}/docs/drafts/project_summary_v1.md

PHASE 2 — Merge all section drafts into a single document:
- Read ALL files in {PROJECT}/docs/drafts/ (specific_aims, significance, innovation, approach_aim1-3, timeline, crosscutting)
- Merge into {PROJECT}/docs/drafts/research_strategy_v1.md following NIH section order
- Resolve terminology conflicts across domain writers
- Ensure one coherent voice, no duplicated background text
- Verify total Research Strategy is within 15-page budget (~7500 words)

REQUIRED INPUTS:
- Project config: {PROJECT}/project.yaml
- Proposal outline: {PROJECT}/docs/outline.md
- All section drafts: {PROJECT}/docs/drafts/*.md
- Literature: {PROJECT}/literature/refs.json and {PROJECT}/literature/gaps.md
- Selected idea: {PROJECT}/ideas/ideas.json
- Style guide: {SYSTEM_DIR}/style_guide.md
- Section specs: {SYSTEM_DIR}/r01_section_specs.md

Do NOT modify state.json — the orchestrator handles tracking."""

EXPECTED_FILES = [
    PROJECT / "docs/drafts/approach_timeline_v1.md",
    PROJECT / "docs/drafts/approach_crosscutting_v1.md",
    PROJECT / "docs/drafts/project_narrative_v1.md",
    PROJECT / "docs/drafts/project_summary_v1.md",
    PROJECT / "docs/drafts/research_strategy_v1.md",
]


async def run_batch_e():
    from nanobot.agent.subagent import SubagentManager
    from nanobot.bus.queue import MessageBus
    from nanobot.config.loader import load_config
    from nanobot.providers.litellm_provider import LiteLLMProvider

    config = load_config()
    model = config.agents.defaults.model
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

    print(f"Model: {model}")
    print(f"Spawning Batch E (integrator assembly)...\n")

    start = time.time()
    result = await mgr.spawn(
        task=ASSEMBLY_PROMPT,
        label="integrator-assembly",
        max_iterations=30,
    )
    print(f"  {result}")

    max_wait = 600
    poll_interval = 15

    while int(time.time() - start) < max_wait:
        await asyncio.sleep(poll_interval)
        elapsed = int(time.time() - start)
        running = mgr.get_running_count()
        found = [f for f in EXPECTED_FILES if f.exists()]
        print(
            f"  [{elapsed:3d}s] running={running}, files={len(found)}/{len(EXPECTED_FILES)}: {[f.name for f in found]}"
        )

        if running == 0:
            print("\nAssembly subagent finished.")
            break

        while not bus.inbound.empty():
            await bus.consume_inbound()

    print("\n=== BATCH E RESULTS ===")
    total_words = 0
    for f in EXPECTED_FILES:
        if f.exists():
            content = f.read_text()
            wc = len(content.split())
            total_words += wc
            print(f"  ✓ {f.name}: {wc} words")
        else:
            print(f"  ✗ {f.name}: MISSING")

    print(
        f"\nTotal: {len([f for f in EXPECTED_FILES if f.exists()])}/{len(EXPECTED_FILES)} files, {total_words} words"
    )
    print(f"Elapsed: {int(time.time() - start)}s")


if __name__ == "__main__":
    asyncio.run(run_batch_e())
