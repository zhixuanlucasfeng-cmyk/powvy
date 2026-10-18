"""Merge raw trending + hand-written analysis -> report.json, data/<date>.json archive and the page.
Usage: python3 build_page.py raw.json analysis.json out_dir [news.json]
news.json (from fetch_news.py) is needed when analysis.json has "news" events."""
import json, pathlib, sys

W = {"popularity": .3, "maintenance": .25, "usability": .25, "virality": .2}
MIN_TODAY = 50

def news_events(ana, items):
    by_url = {i["url"]: i for i in items}
    out = []
    for e in ana.get("news", []):
        src = [by_url[u] for u in e["urls"] if u in by_url]
        if not src:
            continue
        out.append(dict({k: v for k, v in e.items() if k != "urls"}, heat=len({i["source"] for i in src}),
                        published=max(i["published"] for i in src),
                        sources=[{k: i[k] for k in ("source", "tier", "url", "title", "published")} for i in src]))
    out.sort(key=lambda e: (-e["score"], -e["heat"]))
    return out

def build(raw, ana, news_items=()):
    raw = {r["name"]: r for r in raw}
    passed = []
    for name, a in ana["passed"].items():
        r = dict(raw[name], **a)
        r["overall"] = round(sum(a["scores"][k] * w for k, w in W.items()), 1)
        passed.append(r)
    passed.sort(key=lambda r: (-r["overall"], -r["stars_today"]))
    excluded = [{"name": n, "reason": why if isinstance(why, dict) else {"zh": why, "en": why}, "stars_today": raw.get(n, {}).get("stars_today"), "url": f"https://github.com/{n}"}
                for n, why in ana["excluded"].items()]
    return {"date": ana["date"], "weights": W, "min_today": MIN_TODAY, "total_fetched": len(raw),
            "candidates": sum(r["stars_today"] >= MIN_TODAY for r in raw.values()), "projects": passed, "excluded": excluded,
            "news": news_events(ana, news_items), "news_scanned": len(news_items)}

if __name__ == "__main__":
    report = build(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), json.load(open(sys.argv[4])) if len(sys.argv) > 4 else [])
    out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    (out / "data").mkdir(exist_ok=True)
    (out / "data" / f"{report['date']}.json").write_text(json.dumps(report, ensure_ascii=False))
    report["days"] = sorted((p.stem for p in (out / "data").glob("*.json")), reverse=True)
    tpl = (pathlib.Path(__file__).parent.parent / "template.html").read_text()
    assert "/*__DATA__*/null" in tpl
    page = tpl.replace("/*__DATA__*/null", json.dumps(report, ensure_ascii=False).replace("</", "<\\/"))
    (out / "trending.html").write_text(page)  # fragment for Artifact publishing
    (out / "index.html").write_text('<!doctype html>\n<html lang="zh-CN">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + page + "\n</html>\n")
    print(f"{len(report['projects'])} passed, {len(report['excluded'])} excluded, {len(report['news'])} news events -> {out}")
