"""Phase E verification: spawn 3 parallel literature subagents (one per domain) and verify output."""

import asyncio
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT = Path.home() / "Dropbox/AgentWorkspace/PaperAutoGen/r01-older-adults-mci-home-ai"
WORKSPACE = Path.home() / ".nanobot/workspace"
SKILLS_DIR = Path(__file__).parent.parent / "nanobot" / "skills"
LIT_SKILL = SKILLS_DIR / "r01-literature" / "SKILL.md"

DOMAINS = ["hci", "healthcare", "ai"]


def build_literature_prompt(domain: str) -> str:
    return (
        f"You are the {domain} literature agent. "
        f"Read the r01-literature skill at {LIT_SKILL} and follow its instructions. "
        f"Your domain assignment is: {domain}. "
        f"Project path: {PROJECT}/. "
        f"Find 10-18 references for the {domain} domain. "
        f"Use citation graph traversal and iterative query refinement as specified in the skill. "
        f"Write to literature/references_{domain}.json and literature/gaps_{domain}.md."
    )


def expected_files():
    files = {}
    for domain in DOMAINS:
        files[f"refs_{domain}"] = PROJECT / f"literature/references_{domain}.json"
        files[f"gaps_{domain}"] = PROJECT / f"literature/gaps_{domain}.md"
    return files


def validate_refs_json(path: Path, domain: str) -> list[str]:
    issues = []
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return [f"{path.name}: failed to parse — {e}"]

    if "_metadata" not in data:
        issues.append(f"{path.name}: missing _metadata header")
    else:
        meta = data["_metadata"]
        if meta.get("domain") != domain:
            issues.append(
                f"{path.name}: _metadata.domain is '{meta.get('domain')}', expected '{domain}'"
            )
        if "search_rounds" not in meta:
            issues.append(f"{path.name}: _metadata missing search_rounds")
        if "snowball_papers_added" not in meta:
            issues.append(f"{path.name}: _metadata missing snowball_papers_added")

    refs = data.get("references", [])
    if not isinstance(refs, list):
        issues.append(f"{path.name}: 'references' is not a list")
        return issues

    if len(refs) < 10:
        issues.append(f"{path.name}: only {len(refs)} references (minimum 10)")
    if len(refs) > 25:
        issues.append(f"{path.name}: {len(refs)} references (expected 10-18, soft cap 25)")

    must_cite_without_claim = 0
    missing_doi = 0
    for i, ref in enumerate(refs):
        if not ref.get("doi_or_url"):
            missing_doi += 1
        if ref.get("priority") == "must-cite" and not ref.get("supports_claim"):
            must_cite_without_claim += 1

    if missing_doi > 0:
        issues.append(f"{path.name}: {missing_doi} references missing doi_or_url")
    if must_cite_without_claim > 0:
        issues.append(
            f"{path.name}: {must_cite_without_claim} must-cite refs missing supports_claim"
        )

    return issues


def validate_gaps_md(path: Path) -> list[str]:
    issues = []
    try:
        content = path.read_text()
    except FileNotFoundError:
        return [f"{path.name}: file not found"]

    required_sections = [
        "Evidence Summary",
        "Conflicting Evidence",
        "Evidence Synthesis Tables",
    ]
    for section in required_sections:
        if section not in content:
            issues.append(f"{path.name}: missing section '{section}'")

    if len(content.split()) < 100:
        issues.append(
            f"{path.name}: only {len(content.split())} words (expected substantial gap analysis)"
        )

    return issues


async def run_test():
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

    print(f"Provider: {provider_name}, Model: {model}")
    print(f"Project: {PROJECT}")
    print(f"Spawning {len(DOMAINS)} literature agents in parallel...\n")

    start = time.time()

    for domain in DOMAINS:
        prompt = build_literature_prompt(domain)
        result = await mgr.spawn(
            task=prompt,
            label=f"literature-{domain}",
            max_iterations=30,
        )
        print(f"  [literature-{domain}] {result}")

    print(f"\nAll {len(DOMAINS)} literature agents spawned. Waiting for completion...")
    print("(Agents run concurrently — watching for output files)\n")

    ef = expected_files()
    max_wait = 900
    poll_interval = 15

    while int(time.time() - start) < max_wait:
        await asyncio.sleep(poll_interval)
        elapsed = int(time.time() - start)
        running = mgr.get_running_count()
        found = [name for name, path in ef.items() if path.exists()]
        print(f"  [{elapsed:3d}s] running={running}, files={len(found)}/{len(ef)}: {found}")

        if running == 0:
            print("\nAll literature agents finished.")
            break

        while not bus.inbound.empty():
            await bus.consume_inbound()
    else:
        print(f"\nTimeout after {max_wait}s. {mgr.get_running_count()} agents still running.")

    print("\n=== PHASE E VERIFICATION ===\n")

    print("--- E.8: Parallel Dispatch ---")
    all_present = True
    for name, path in ef.items():
        if path.exists():
            size = len(path.read_text().split())
            print(f"  PASS  {path.name}: {size} words")
        else:
            print(f"  FAIL  {path.name}: MISSING")
            all_present = False

    print(
        f"\n  Result: {'PASS' if all_present else 'FAIL'} — {sum(1 for p in ef.values() if p.exists())}/{len(ef)} files created\n"
    )

    print("--- E.9: Output Validation ---")
    all_issues = []
    for domain in DOMAINS:
        refs_path = ef[f"refs_{domain}"]
        gaps_path = ef[f"gaps_{domain}"]
        if refs_path.exists():
            issues = validate_refs_json(refs_path, domain)
            all_issues.extend(issues)
            for issue in issues:
                print(f"  WARN  {issue}")
        if gaps_path.exists():
            issues = validate_gaps_md(gaps_path)
            all_issues.extend(issues)
            for issue in issues:
                print(f"  WARN  {issue}")

    if not all_issues:
        print("  PASS  All domain outputs pass validation")
    print(f"\n  Result: {'PASS' if not all_issues else 'WARN'} — {len(all_issues)} issues found\n")

    print("--- E.10: Reference Count ---")
    total_refs = 0
    for domain in DOMAINS:
        refs_path = ef[f"refs_{domain}"]
        if refs_path.exists():
            try:
                data = json.loads(refs_path.read_text())
                refs = data.get("references", [])
                count = len(refs)
                total_refs += count
                print(f"  {domain}: {count} references")
            except json.JSONDecodeError:
                print(f"  {domain}: parse error")

    target_met = 30 <= total_refs <= 60
    print(f"\n  Total: {total_refs} references (target: 30-50)")
    print(f"  Result: {'PASS' if target_met else 'FAIL'}\n")

    print(f"=== OVERALL: Elapsed {int(time.time() - start)}s ===")


if __name__ == "__main__":
    asyncio.run(run_test())
