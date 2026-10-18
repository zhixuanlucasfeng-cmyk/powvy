"""Fetch recent items from the AI news feeds in news_sources.json (source list from AIHOT, MIT).
Usage: python3 fetch_news.py out.json [hours=48]"""
import gzip, html, json, pathlib, re, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

HOURS = int(sys.argv[2]) if len(sys.argv) > 2 else 48
SOURCES = json.loads((pathlib.Path(__file__).parent.parent / "news_sources.json").read_text())

def when(s):
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

def items(xml):
    root = ET.fromstring(xml)
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        f = {c.tag.split("}")[-1]: c for c in el}
        link = f.get("link")
        url = (link.get("href") or link.text or "").strip() if link is not None else ""
        date = next((f[k].text for k in ("pubDate", "published", "updated", "date") if k in f and f[k].text), None)
        body = next((f[k].text for k in ("description", "summary", "content", "encoded") if k in f and f[k].text), "")
        yield {"title": text(f["title"].text if "title" in f else ""), "url": url, "published": date, "summary": text(body)[:700]}

cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS)
out = []
for s in SOURCES:
    try:
        req = urllib.request.Request(s["url"], headers={"User-Agent": "Mozilla/5.0 (powvy news fetcher)"})
        raw = urllib.request.urlopen(req, timeout=30).read()
        got = list(items(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw))  # some feeds gzip regardless of Accept-Encoding
    except Exception as e:
        print(f"skip {s['name']}: {e}", file=sys.stderr); continue
    fresh = [i for i in got if (d := when(i["published"])) and d >= cutoff]
    for i in fresh:
        i.update(source=s["name"], tier=s["tier"], published=when(i["published"]).isoformat())
    out += fresh
    print(f"{s['name']}: {len(fresh)}/{len(got)}", file=sys.stderr)
out.sort(key=lambda i: i["published"], reverse=True)
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(f"{len(out)} items from the last {HOURS}h -> {sys.argv[1]}")
