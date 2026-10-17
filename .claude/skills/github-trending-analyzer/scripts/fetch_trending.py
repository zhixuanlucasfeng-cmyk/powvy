"""Fetch GitHub Trending (all + zh + per-language boards), merge, enrich candidates via GitHub API.
Usage: python3 fetch_trending.py out.json"""
import html, json, os, re, subprocess, sys, urllib.request

def get(url):
    h = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok and url.startswith("https://api.github.com/"):
        h["Authorization"] = "Bearer " + tok
    req = urllib.request.Request(url, headers=h)
    return urllib.request.urlopen(req, timeout=30).read().decode()

def num(s):
    return int(re.sub(r"[^\d]", "", s) or 0)

def parse(page, board):
    out = []
    for row in page.split('<article class="Box-row">')[1:]:
        name = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', row).group(1)
        desc = re.search(r'<p class="col-9[^"]*">(.*?)</p>', row, re.S)
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)', row)
        stars = re.search(r'href="/[^"]+/stargazers"[^>]*>.*?</svg>\s*([\d,]+)', row, re.S)
        today = re.search(r'([\d,]+)\s+stars (?:today|this week|this month)', row)
        out.append({"name": name, "description": html.unescape(re.sub(r"<[^>]+>", "", desc.group(1))).strip() if desc else "",
                    "language": lang.group(1).strip() if lang else None, "stars": num(stars.group(1)) if stars else 0,
                    "stars_today": num(today.group(1)) if today else 0, "url": f"https://github.com/{name}", "boards": [board]})
    return out

def gh_api(path):
    try:  # gh CLI is authenticated (5000/h); fall back to anonymous API (60/h)
        return json.loads(subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True).stdout)
    except Exception:
        return json.loads(get("https://api.github.com/" + path))

MIN_TODAY = 50  # below this a repo is not a candidate and is not enriched
LANGS = ["python", "typescript", "javascript", "rust", "go", "jupyter-notebook", "c++", "java", "swift", "kotlin", "c", "c%23", "shell", "dart"]
T = "https://github.com/trending"
BOARDS = [("all", T + "?since=daily"), ("zh", T + "?since=daily&spoken_language_code=zh")] + [(l, f"{T}/{l}?since=daily") for l in LANGS]

merged = {}
for board, url in BOARDS:
    try:
        rows = parse(get(url), board)
    except Exception as e:
        print(f"skip {board}: {e}", file=sys.stderr); continue
    for r in rows:
        if r["name"] in merged:
            merged[r["name"]]["boards"].append(board)
        else:
            merged[r["name"]] = r
for r in merged.values():
    if r["stars_today"] < MIN_TODAY:
        continue
    try:
        m = gh_api(f"repos/{r['name']}")
        r.update(pushed_at=m.get("pushed_at"), created_at=m.get("created_at"), topics=m.get("topics", []),
                 license=(m.get("license") or {}).get("spdx_id"), forks=m.get("forks_count"), open_issues=m.get("open_issues_count"),
                 archived=m.get("archived"), homepage=m.get("homepage"))
    except Exception as e:
        r["api_error"] = str(e)
json.dump(list(merged.values()), open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(f"{len(merged)} unique repos, {sum(r['stars_today'] >= MIN_TODAY for r in merged.values())} with >= {MIN_TODAY} stars today -> {sys.argv[1]}")
