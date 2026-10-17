---
name: github-trending-analyzer
description: Use when the user says "分析今日GitHub热门项目", asks to analyze/pick projects from today's GitHub Trending, or when the daily routine runs. Fetches all-language + Chinese trending, filters, scores from READMEs, and publishes the page to the Powvy site at /trending/.
---

# GitHub Trending Analyzer

Lives in the Powvy site repo (`zhixuanlucasfeng-cmyk/powvy`). Output goes to `trending/` in that repo, served at https://zhixuanlucasfeng-cmyk.github.io/powvy/trending/. The page is bilingual (follows the site's 中/EN toggle via `powvy-lang`), so every text field is written in Chinese and English.

`$SKILL` = this directory. `$W` = a scratch dir outside the repo (e.g. `/tmp/gt`).

## 1. Fetch
```bash
python3 $SKILL/scripts/fetch_trending.py $W/raw.json
```
Parses the daily all-language board, the Chinese board (`zh`) and 14 language boards (python, typescript, rust, go…), merges duplicates (`boards: ["all","zh","python"]`), and enriches repos with ≥ 50 stars today via `gh api`, or the GitHub API with `$GITHUB_TOKEN` if set, else anonymously (60 requests/h; repos past the limit get `api_error` and no pushed_at, so judge maintenance from the README) (pushed_at, license, forks, topics). Takes 2–4 min.

## 2. Filter (record every exclusion with a zh + en reason)
- `stars_today < 50` → not a candidate, drop silently (not listed as excluded)
- `pushed_at` older than one year, or `archived` → exclude
- Exclude by README/description: resource collections / awesome lists / plugin directories, interview questions, tutorials & config collections, pure low-level libraries, translations, obvious star-farmed marketing shells (very new + huge stars + tiny watchers/forks + empty README). Borderline → keep, note the doubt in `cautions`, lower `popularity`.
- Keep at most **50**: the survivors with the most stars today. The rest are excluded with reason `今日新增 N，未进前 50` / `N stars today, outside the top 50`.
- Analyses from earlier days can be reused for repos that are still trending (copy from the previous `trending/data/<date>.json`).

## 3. Read READMEs and score
For each survivor read the top ~150 lines of the README. Prefer the raw file, which has no API rate limit: `curl -sL https://raw.githubusercontent.com/<name>/HEAD/README.md` (try `readme.md` / `README.rst` if 404). Otherwise:
`curl -sL -H "Accept: application/vnd.github.raw" https://api.github.com/repos/<name>/readme` (or `gh api repos/<name>/readme -H "Accept: application/vnd.github.raw"`).
Score 1–10: `popularity` (today's stars, total, forks/watchers sanity), `maintenance` (last push, cadence), `usability` (install effort, prerequisites, paid deps), `virality` (story, demo, appeal). The build script computes overall (weights .3/.25/.25/.2).

Write `$W/analysis.json`:
```json
{"date": "YYYY-MM-DD",
 "passed": {"owner/repo": {"scores": {"popularity": 9, "maintenance": 9, "usability": 8, "virality": 9},
   "cats": ["agent", "claude"], "stack": "技术栈", "type": "项目类型", "usage": "使用方式（可用 `code`）",
   "highlights": ["核心亮点"], "cautions": ["注意事项"],
   "en": {"stack": "...", "type": "...", "usage": "...", "highlights": ["..."], "cautions": ["..."]}}},
 "excluded": {"owner/repo": {"zh": "今日新增 62 < 100；且为教程", "en": "62 stars today < 100; tutorial"}}}
```
`cats`: 1–3 of `agent` (AI agents), `claude` (Claude Code ecosystem / skills / plugins), `coding` (coding tools), `memory` (memory, RAG), `llm` (models, inference), `media` (audio, video, image), `data` (data, scraping, trading), `infra` (infra, DevOps), `security`, `app` (apps, productivity). The page filters by these and by `language`.
Facts come from the README only, no invented claims. The `en` block is a faithful English version of the same facts. Use today's UTC date.

## 4. Build
```bash
python3 $SKILL/scripts/build_page.py $W/raw.json $W/analysis.json trending
```
Writes `trending/index.html` (standalone page, Powvy manga style from `template.html`), `trending/report.json` (structured JSON), `trending/data/<date>.json` (daily archive; the page's day picker lists every file there), and `trending/trending.html` (Artifact fragment, gitignored). Don't edit the template per run.

## 5. Publish
Commit only `trending/index.html`, `trending/report.json` and `trending/data/` with message `trending: YYYY-MM-DD`, and push to `main` (GitHub Pages deploys from main). No Co-Authored-By / Claude attribution lines. When run interactively, also reply with a top-5 table (综合分 / 今日新增 / 一句话亮点) and the page URL.
