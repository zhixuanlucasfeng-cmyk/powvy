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

## JC public gateway follow-up

- Published `https://jc.powvy.org/scoreboard` through the fixed-origin Worker in `project-gateway/`. It fetches the existing public Vercel production deployment; no database migration or protection changes.
- Chrome rendered real house standings, the scorer login page, and redirected unauthenticated `/events` to `/login`. Mobile width and public-page navigation checked. No real scores edited.
- Vercel replaces `X-Forwarded-Host`, which initially broke Next Server Actions. The gateway translates only an exact same-origin Origin to its fixed upstream; foreign/null origins are preserved. Regression tests cover this boundary, auth status/cookies, redirects and unavailable responses.
- School Wi-Fi still requires verification on the affected visitor's computer. A successful local check does not guarantee every network.

## Rest Solar remains blocked

- The current company website uses `rest-solar-agent-cm.onrender.com`, while the old portfolio entry uses `rest-solar-agent.onrender.com`.
- Direct connections time out here. A test Worker targeting the current CM backend receives HTTP 429 with `cf-mitigated: challenge`, not a working chat application. It has not been linked from the portfolio or assigned a public custom domain.
- Render CLI credentials have expired (API 401). Requested owner reauthentication before inspecting service health/configuration. No secrets copied, challenges bypassed, login protections removed, or customer data changed.

## Rest Solar restored entry (later check, 10 Nov)

- Render dashboard became reachable (HTTP 200). The old `rest-solar-agent.onrender.com` health endpoint still timed out, but the current CM service returned `{"status":"ok"}`. No Render settings were changed: the CLI authorization had not completed.
- The existing gateway's upstream challenge was no longer present. A real English product-information chat returned HTTP 200 and a substantive reply. Published the native Cloudflare custom domain `solar-agent.powvy.org`, pointing only at the existing CM backend.
- Chrome on the new domain: `/` redirects to `/chat`, mobile 390px layout has no horizontal overflow, French language toggle and a real French product-information reply work, no JavaScript exceptions. Synthetic tests did not place orders or request staff contact.
- Updated portfolio, connection diagnostics and public AI project facts to the verified online entry, and removed the outdated timeout badge. This fixes the stale portfolio destination; it is not evidence that Render can never time out or that school-network filtering is resolved.
- Worker version: `f20b76ec-805a-405f-82f2-293a75e1be5d`. Existing Render database, admin accounts and security controls unchanged.
