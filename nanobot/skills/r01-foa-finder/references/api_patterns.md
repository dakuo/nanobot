# FOA Finder API Reference

## Grants.gov Search2 API

No authentication required. All calls use `exec` with `curl`.

### Keyword Search

```bash
curl -s -X POST 'https://api.grants.gov/v1/api/search2' \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"{KEYWORDS}","oppStatuses":"posted","rows":50}' \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'TOTAL: {d[\"data\"][\"hitCount\"]}')
for h in d['data']['oppHits']:
  if 'NIH' not in h.get('agencyCode',''): continue
  cfdas=','.join(h.get('cfdaList',[]))
  print(f'{h[\"number\"]}|{h[\"title\"]}|{h.get(\"closeDate\",\"\")}|{cfdas}|{h[\"id\"]}|{h[\"oppStatus\"]}')
"
```

- Replace `{KEYWORDS}` with topic phrase (e.g., `"clinical informatics"`)
- Do NOT add `agencies` or `fundingCategories` filters — they break NIH results
- The python filter keeps only NIH results and outputs a compact pipe-delimited format
- Output format: `FOA_NUMBER|TITLE|CLOSE_DATE|ALN_LIST|GRANTS_GOV_ID|STATUS`

**IMPORTANT**: The `exec` tool truncates output at 10,000 characters. Raw JSON responses are 18-27K chars and WILL be truncated, causing you to miss FOAs. Always use the python post-processing pipe shown above — it reduces output to ~3-8K chars (safe).

### CFDA/ALN Search (by institute)

```bash
curl -s -X POST 'https://api.grants.gov/v1/api/search2' \
  -H 'Content-Type: application/json' \
  -d '{"cfda":"{ALN_NUMBER}","oppStatuses":"posted","rows":50}' \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'TOTAL: {d[\"data\"][\"hitCount\"]}')
for h in d['data']['oppHits']:
  cfdas=','.join(h.get('cfdaList',[]))
  print(f'{h[\"number\"]}|{h[\"title\"]}|{h.get(\"closeDate\",\"\")}|{cfdas}|{h[\"id\"]}|{h[\"oppStatus\"]}')
"
```

- Replace `{ALN_NUMBER}` with the ALN for the target IC (e.g., `"93.879"` for NLM)
- Returns ALL active FOAs from that institute — no keyword filtering needed
- Use ALN→IC table below to pick the right number
- The python pipe is REQUIRED — raw JSON for CFDA searches exceeds the 10K truncation limit

### Exact FOA Number Lookup

```bash
curl -s -X POST 'https://api.grants.gov/v1/api/search2' \
  -H 'Content-Type: application/json' \
  -d '{"oppNum":"{FOA_NUMBER}","oppStatuses":"posted|forecasted|closed|archived","rows":1}'
```

- Replace `{FOA_NUMBER}` with exact FOA (e.g., `"PAR-25-235"`)
- Include all statuses to detect closed/archived FOAs (for reissue chain detection)

### Response Fields

```
data.hitCount          → total results (integer)
data.oppHits[]         → array of opportunities:
  .id                  → grants.gov internal ID (use for detail page URL)
  .number              → FOA number (e.g., "PAR-25-235")
  .title               → full title
  .agencyCode          → "HHS-NIH11" for NIH
  .openDate            → "MM/DD/YYYY"
  .closeDate           → "MM/DD/YYYY"
  .oppStatus           → "posted" | "forecasted" | "closed" | "archived"
  .cfdaList[]          → array of ALN strings (e.g., ["93.242", "93.879"])
```

**Validation rule**: If `hitCount` is 0 for a keyword search, the query may be too narrow. Try a broader keyword before concluding no FOAs exist.

---

## NIH Reporter v2 API

No authentication required. Rate limit: 1-second pause between calls.

### Search Funded Projects

```bash
curl -s -X POST 'https://api.reporter.nih.gov/v2/projects/search' \
  -H 'Content-Type: application/json' \
  -d '{
    "criteria": {
      "advanced_text_search": {
        "operator": "and",
        "search_field": "all",
        "search_text": "{TOPIC_KEYWORDS}"
      },
      "activity_codes": ["R01"],
      "fiscal_years": [2024, 2025, 2026],
      "include_active_projects": true
    },
    "include_fields": [
      "OpportunityNumber",
      "AgencyIcAdmin",
      "ProjectTitle",
      "ProjectNum",
      "ProgramOfficers",
      "FiscalYear"
    ],
    "limit": 50
  }'
```

- Replace `{TOPIC_KEYWORDS}` with topic phrase
- Do NOT include `agencies` filter in the first search — let results reveal which ICs fund this topic
- After discovering top ICs, optionally run a second search with `"agencies": ["{IC}"]`

### Search by FOA Number (reverse lookup)

```bash
curl -s -X POST 'https://api.reporter.nih.gov/v2/projects/search' \
  -H 'Content-Type: application/json' \
  -d '{
    "criteria": {
      "opportunity_numbers": ["{FOA_NUMBER}"],
      "activity_codes": ["R01"]
    },
    "include_fields": [
      "ProjectTitle",
      "AgencyIcAdmin",
      "PrincipalInvestigators",
      "ProgramOfficers",
      "FiscalYear"
    ],
    "limit": 20
  }'
```

### Response Fields

```
meta.total             → total matching projects (integer)
results[]              → array of projects:
  .opportunity_number  → FOA number this project was funded under
  .agency_ic_admin     → object: { .abbreviation: "NLM", .name: "..." }
  .project_num         → grant number (e.g., "1R01LM014345-01")
  .project_title       → title string
  .program_officers[]  → array: { .first_name, .last_name }
  .fiscal_year         → integer
```

---

## FOA Enrichment URLs

### Strategy: Try each source in order. NEVER discard a FOA just because enrichment fails.

If all enrichment attempts fail, include the FOA in your output using the data from the search2 response (number, title, close date, ALN list). Partial information is always better than dropping a valid FOA.

### 1. NIH Guide (works for most pre-2026 FOAs)

Construct URL based on FOA type prefix:

| Prefix | URL Pattern |
|--------|-------------|
| PA, PAR, PAS | `https://grants.nih.gov/grants/guide/pa-files/{FOA_NUMBER}.html` |
| RFA | `https://grants.nih.gov/grants/guide/rfa-files/{FOA_NUMBER}.html` |
| NOT | `https://grants.nih.gov/grants/guide/notice-files/{FOA_NUMBER}.html` |

Use `web_fetch` (GET) to retrieve. If 404 (common for 2026+ FOAs), proceed to next source.

### 2. Web search for full announcement (best for 2026+ FOAs)

```
web_search("{FOA_NUMBER} full announcement NIH")
```

This typically returns a link to the full announcement on `files.simpler.grants.gov`. These are static HTML pages that `web_fetch` can read. Look for URLs matching:
```
https://files.simpler.grants.gov/opportunities/.../.../{FOA_NUMBER}-Full-Announcement.html
```

### 3. Grants.gov Detail Page (last resort)

```
https://www.grants.gov/search-results-detail/{GRANTS_GOV_ID}
```

Replace `{GRANTS_GOV_ID}` with the `id` field from the search2 response. Note: this is a JavaScript-rendered page — `web_fetch` may return limited content. Use it only if sources 1 and 2 fail.

---

## ALN → IC Mapping

Use these Assistance Listing Numbers (formerly CFDA) to search Grants.gov for all FOAs from a specific NIH institute.

| IC | ALN | Full Name |
|----|-----|-----------|
| NLM | 93.879 | National Library of Medicine |
| NIBIB | 93.286 | National Institute of Biomedical Imaging and Bioengineering |
| NIMH | 93.242 | National Institute of Mental Health |
| NCI | 93.394 | National Cancer Institute |
| NHLBI | 93.837 | National Heart, Lung, and Blood Institute |
| NIA | 93.866 | National Institute on Aging |
| NIDDK | 93.847 | National Institute of Diabetes and Digestive and Kidney Diseases |
| NINDS | 93.853 | National Institute of Neurological Disorders and Stroke |
| NHGRI | 93.172 | National Human Genome Research Institute |
| NIAID | 93.855 | National Institute of Allergy and Infectious Diseases |
| NIGMS | 93.859 | National Institute of General Medical Sciences |
| NIDA | 93.279 | National Institute on Drug Abuse |
| NIMHD | 93.307 | National Institute on Minority Health and Health Disparities |
| NCATS | 93.350 | National Center for Advancing Translational Sciences |
| NICHD | 93.865 | Eunice Kennedy Shriver National Institute of Child Health and Human Development |
| OD | 93.310 | Office of the Director |
| NEI | 93.867 | National Eye Institute |
| NIEHS | 93.113 | National Institute of Environmental Health Sciences |
| NIDCR | 93.121 | National Institute of Dental and Craniofacial Research |
| NIDCD | 93.173 | National Institute on Deafness and Other Communication Disorders |

Some ICs have multiple ALNs (e.g., NHLBI also uses 93.838, 93.839). The primary ALN listed above covers most R01 FOAs.

---

## IC Code ↔ FOA Number Prefix

The 2-letter code in targeted FOA numbers (e.g., PAR-**LM**-26-001) maps to the issuing IC:

| FOA Prefix | IC |
|------------|----|
| LM | NLM |
| EB | NIBIB |
| MH | NIMH |
| CA | NCI |
| HL | NHLBI |
| AG | NIA |
| DK | NIDDK |
| NS | NINDS |
| HG | NHGRI |
| AI | NIAID |
| GM | NIGMS |
| DA | NIDA |
| MD | NIMHD |
| TR | NCATS |
| HD | NICHD |
| OD | OD |

Note: NIH-wide FOAs (PA-25-301, PAR-25-235) do NOT contain an IC prefix — the issuing/participating ICs are listed in the FOA body text.

---

## Parent R01 FOAs

When no targeted PAR/RFA is found, recommend the appropriate Parent R01 based on clinical trial classification:

| Clinical Trial Classification | Parent R01 | Description |
|-------------------------------|-----------|-------------|
| `not_allowed` | PA-25-301 | Research Projects (Clinical Trial Not Allowed) |
| `optional` | PA-25-302 | Research Projects (Clinical Trial Optional) |
| `required` | PA-25-303 | Research Projects (Clinical Trial Required) |

Standard R01 budget: up to $500,000/year direct costs (requests exceeding this require prior IC approval).
