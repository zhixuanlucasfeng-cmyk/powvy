"""Merge raw trending + hand-written analysis -> report.json + crayon page.
Usage: python3 build_page.py raw.json analysis.json out_dir"""
import json, pathlib, sys

W = {"popularity": .3, "maintenance": .25, "usability": .25, "virality": .2}

def build(raw, ana):
    raw = {r["name"]: r for r in raw}
    passed = []
    for name, a in ana["passed"].items():
        r = dict(raw[name], **a)
        r["overall"] = round(sum(a["scores"][k] * w for k, w in W.items()), 1)
        passed.append(r)
    passed.sort(key=lambda r: (-r["overall"], -r["stars_today"]))
    excluded = [{"name": n, "reason": why, "stars_today": raw.get(n, {}).get("stars_today"), "url": f"https://github.com/{n}"}
                for n, why in ana["excluded"].items()]
    return {"date": ana["date"], "weights": W, "total_fetched": len(raw), "projects": passed, "excluded": excluded}

if __name__ == "__main__":
    report = build(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])))
    out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    tpl = (pathlib.Path(__file__).parent.parent / "template.html").read_text()
    assert "/*__DATA__*/null" in tpl
    page = tpl.replace("/*__DATA__*/null", json.dumps(report, ensure_ascii=False).replace("</", "<\\/"))
    (out / "trending.html").write_text(page)  # fragment for Artifact publishing
    (out / "index.html").write_text('<!doctype html>\n<html lang="zh-CN">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + page + "\n</html>\n")
    print(f"{len(report['projects'])} passed, {len(report['excluded'])} excluded -> {out}")
