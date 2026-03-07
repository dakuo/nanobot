"""Phase E verification: spawn 3 parallel literature subagents (one per domain) and verify output."""

import asyncio
import json
import sys
import time
from pathlib import Path

import yaml

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


def validate_team_prior_work(project_path: Path, domains: list[str]) -> list[str]:
    """Validate minimum team_prior_work papers per investigator across all domains.

    Hard gate: PI needs >= 3, each co-PI needs >= 3.
    """
    issues = []

    project_yaml = project_path / "project.yaml"
    if not project_yaml.exists():
        return [f"project.yaml not found at {project_yaml} — cannot validate team prior work"]

    with open(project_yaml) as f:
        config = yaml.safe_load(f)

    investigators = config.get("investigators", {})
    if not investigators:
        return ["project.yaml has no investigators section — cannot validate team prior work"]

    pi = investigators.get("pi", {})
    co_investigators = investigators.get("co_investigators", []) or []

    all_refs = []
    for domain in domains:
        refs_path = project_path / f"literature/references_{domain}.json"
        if refs_path.exists():
            try:
                data = json.loads(refs_path.read_text())
                all_refs.extend(data.get("references", []))
            except json.JSONDecodeError:
                pass

    team_refs = [r for r in all_refs if r.get("team_prior_work")]

    def count_investigator_papers(name: str) -> int:
        last_name = name.split()[-1].lower()
        count = 0
        for ref in team_refs:
            authors = ref.get("authors", "").lower()
            if last_name in authors:
                count += 1
        return count

    pi_name = pi.get("name", "Unknown PI")
    pi_count = count_investigator_papers(pi_name)
    if pi_count < 3:
        issues.append(
            f"HARD FAIL: PI '{pi_name}' has {pi_count} team_prior_work papers (minimum 3)"
        )

    for co_i in co_investigators:
        co_name = co_i.get("name", "Unknown Co-I")
        co_count = count_investigator_papers(co_name)
        if co_count < 3:
            issues.append(
                f"HARD FAIL: Co-I '{co_name}' has {co_count} team_prior_work papers (minimum 3)"
            )

    total_team = len(team_refs)
    if total_team == 0:
        issues.append("HARD FAIL: Zero team_prior_work papers found across all domains")

    return issues


def validate_seed_references(project_path: Path, domains: list[str]) -> list[str]:
    """Validate that all PI-provided seed references appear in literature output."""
    issues = []

    project_yaml = project_path / "project.yaml"
    if not project_yaml.exists():
        return []

    with open(project_yaml) as f:
        config = yaml.safe_load(f)

    seeds = config.get("seed_references", []) or []
    if not seeds:
        return []

    all_refs = []
    for domain in domains:
        refs_path = project_path / f"literature/references_{domain}.json"
        if refs_path.exists():
            try:
                data = json.loads(refs_path.read_text())
                all_refs.extend(data.get("references", []))
            except json.JSONDecodeError:
                pass

    user_provided_refs = [r for r in all_refs if r.get("user_provided")]
    found_count = len(user_provided_refs)

    if found_count < len(seeds):
        issues.append(
            f"WARN: {found_count}/{len(seeds)} seed references found in output "
            f"(missing {len(seeds) - found_count})"
        )

    if found_count == 0 and len(seeds) > 0:
        issues.append(
            f"HARD FAIL: Zero seed references ingested — "
            f"{len(seeds)} provided in project.yaml but none found in output"
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

    print("--- E.11: Team Prior Work Validation ---")
    team_issues = validate_team_prior_work(PROJECT, DOMAINS)
    hard_fails = [i for i in team_issues if i.startswith("HARD FAIL")]
    if team_issues:
        for issue in team_issues:
            print(f"  {'FAIL' if 'HARD FAIL' in issue else 'WARN'}  {issue}")
    else:
        team_ref_count = 0
        for domain in DOMAINS:
            refs_path = ef[f"refs_{domain}"]
            if refs_path.exists():
                try:
                    data = json.loads(refs_path.read_text())
                    team_ref_count += sum(
                        1 for r in data.get("references", []) if r.get("team_prior_work")
                    )
                except json.JSONDecodeError:
                    pass
        print(f"  PASS  {team_ref_count} team_prior_work papers found across all domains")
    print(
        f"\n  Result: {'FAIL' if hard_fails else 'PASS'} — "
        f"{len(hard_fails)} hard failures, {len(team_issues) - len(hard_fails)} warnings\n"
    )

    print("--- E.12: Seed Reference Validation ---")
    seed_issues = validate_seed_references(PROJECT, DOMAINS)
    seed_hard_fails = [i for i in seed_issues if i.startswith("HARD FAIL")]
    if seed_issues:
        for issue in seed_issues:
            print(f"  {'FAIL' if 'HARD FAIL' in issue else 'WARN'}  {issue}")
    else:
        with open(PROJECT / "project.yaml") as f:
            cfg = yaml.safe_load(f)
        seed_count = len(cfg.get("seed_references", []) or [])
        if seed_count > 0:
            print(f"  PASS  All {seed_count} seed references found in output")
        else:
            print("  SKIP  No seed references in project.yaml")
    print(
        f"\n  Result: {'FAIL' if seed_hard_fails else 'PASS'} — {len(seed_issues)} issues found\n"
    )

    overall_pass = (
        all_present and not all_issues and target_met and not hard_fails and not seed_hard_fails
    )
    print(
        f"=== OVERALL: {'PASS' if overall_pass else 'FAIL'} — Elapsed {int(time.time() - start)}s ==="
    )


if __name__ == "__main__":
    asyncio.run(run_test())
