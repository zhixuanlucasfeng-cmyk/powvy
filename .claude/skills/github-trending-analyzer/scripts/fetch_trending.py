"""Fetch GitHub Trending (all + zh), merge, enrich via GitHub API. Usage: python3 fetch_trending.py out.json"""
import html, json, re, subprocess, sys, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"})
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

merged = {}
for board, q in [("all", ""), ("zh", "&spoken_language_code=zh")]:
    for r in parse(get("https://github.com/trending?since=daily" + q), board):
        if r["name"] in merged:
            merged[r["name"]]["boards"].append(board)
        else:
            merged[r["name"]] = r
for r in merged.values():
    try:
        m = gh_api(f"repos/{r['name']}")
        r.update(pushed_at=m.get("pushed_at"), created_at=m.get("created_at"), topics=m.get("topics", []),
                 license=(m.get("license") or {}).get("spdx_id"), forks=m.get("forks_count"), open_issues=m.get("open_issues_count"),
                 archived=m.get("archived"), homepage=m.get("homepage"))
    except Exception as e:
        r["api_error"] = str(e)
json.dump(list(merged.values()), open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(f"{len(merged)} unique repos -> {sys.argv[1]}")
