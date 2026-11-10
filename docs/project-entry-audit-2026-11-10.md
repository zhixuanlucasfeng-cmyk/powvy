# Project entry audit — 2026-11-10

Checked all 16 personal-site product detail routes in Chinese and English; 17 distinct external/internal destination URLs before adding the Rest Solar source fallback. Browser navigation checked actual body content, not just HTTP status. All 11 open-source repository links returned HTTP 200 without signing in. School-network reachability is not guaranteed by these checks.

| Project | Destination | Observation |
|---|---|---|
| Powvy Badminton | https://powvybadminton.com/ | HTTP 200; page content rendered |
| JC Sports Day Scoring | https://github.com/zhixuanlucasfeng-cmyk/jc-sports-day | HTTP 200; page content rendered |
| Powvy 热榜 | https://powvy.org/trending/index.html | HTTP 200; page content rendered |
| Powvy Habit | https://zhixuanlucasfeng-cmyk.github.io/liangli/ | HTTP 200; page content rendered |
| Chainsaw Man Philosophy | https://zhixuanlucasfeng-cmyk.github.io/Chainsaw-man-philosophy/ | HTTP 200; blank body |
| JC Sports Day Scoring | https://jc-sports-day-scoring.vercel.app/scoreboard | page.goto: Timeout 22000ms exceeded. |
| JC Sports Day Scoring | https://jc-sports-day-scoring.vercel.app/login | page.goto: Timeout 22000ms exceeded. |
| A-Level Survival Bureau | https://alevel-survival-bureau.vercel.app/ | HTTP 200; page content rendered |
| DryRun | https://dryruncs.com/ | HTTP 200; page content rendered |
| Powvy AI Agent / Power | https://github.com/zhixuanlucasfeng-cmyk/power | HTTP 200; page content rendered |
| Claude Usage | https://github.com/zhixuanlucasfeng-cmyk/claude-usage | HTTP 200; page content rendered |
| Powvy Note | https://github.com/zhixuanlucasfeng-cmyk/powvy-note | HTTP 200; page content rendered |
| Colorbook | https://zhixuanlucasfeng-cmyk.github.io/colorbook/ | HTTP 200; page content rendered |
| Contract | https://github.com/zhixuanlucasfeng-cmyk/contract | HTTP 200; page content rendered |
| Legend of 4P Vedundi | https://zhixuanlucasfeng-cmyk.github.io/legend-of-4p-vedundi/ | HTTP 200; page content rendered |
| Camaroom Web | https://zhixuanlucasfeng-cmyk.github.io/camaroom-web/ | HTTP 200; page content rendered |
| Rest Solar Agent | https://rest-solar-agent.onrender.com/ | page.goto: Timeout 22000ms exceeded. |

## Repairs and remaining limitations

- Chainsaw Man Philosophy: published `gh-pages` branch had root-relative asset/image paths and a root-only app router. Fixed its project base. Also removed a blocking Google Fonts CSS import and deferred optional font loading; fixed an undeclared ads variable that crashed React when the ad script was blocked. Browser regression passes with fonts indefinitely stalled and ads unavailable. Repair commit: 2a53d10. This repairs the prebuilt deployment branch; it does not claim the separate, incomplete main-branch source build was fixed.
- Camaroom Web now links directly to its verified redirect destination, https://restarsolar.net/.
- JC and Rest Solar Agent: live connections still timed out. Kept live URLs, added dated bilingual access notices, and provided verified public source links instead of claiming restored service.
- Source-only local apps now explicitly say installation is required; a GitHub repository is not presented as a running web app.
- A-Level rendered successfully in this audit. Its earlier intermittent connection issue and reported school-network blank page remain unverified on the affected computer.
- No school-network restrictions, certificate checks, or browser security controls were bypassed.
