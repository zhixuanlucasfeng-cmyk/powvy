# Project entry recheck — 2026-11-10

Anonymous Chrome check from this computer, not the affected school network. HTTP success alone is not treated as usable content.

| Entry | HTTP | Body / errors |
|---|---|---|
| https://powvybadminton.com/ | 200 | Rendered content; 0 JS errors |
| https://jc.powvy.org/login | 200 | Rendered content; 0 JS errors |
| https://powvy.org/trending/index.html | 200 | Rendered content; 0 JS errors |
| https://zhixuanlucasfeng-cmyk.github.io/liangli/ | 200 | Rendered content; 0 JS errors |
| https://jc.powvy.org/scoreboard | 200 | Rendered content; 0 JS errors |
| https://zhixuanlucasfeng-cmyk.github.io/Chainsaw-man-philosophy/ | 200 | Blank; runtime error ['Vl'] |
| https://alevel-survival-bureau.vercel.app/ | 200 | Rendered content; 0 JS errors |
| https://dryruncs.com/ | 200 | Rendered content; 0 JS errors |
| https://solar-agent.powvy.org/ | 429 | 429 unavailable |
| https://zhixuanlucasfeng-cmyk.github.io/legend-of-4p-vedundi/ | 200 | Rendered content; 0 JS errors |
| https://zhixuanlucasfeng-cmyk.github.io/colorbook/ | 200 | Rendered content; 0 JS errors |
| https://restarsolar.net/ | 200 | Rendered content; 0 JS errors |

All 13 unique source/download URLs returned HTTP 200 (redirects followed); this confirms availability, not installation or application operation. Five product entries are local/installable tools, and are labelled accordingly.

## Findings and changes

- Philosophy intermittently crashed during React rendering when the placeholder AdSense provider threw. Removed ad loading and the render-time push from the deployed gh-pages artifact, including the 404 entry; versioned the JS URL. Simulated a throwing ad provider: body rendered with no JS errors. Commit 596e042. Source main remains outside this artifact repair.
- Rest Solar returned HTTP 429 in the first browser pass; the direct CM app and gateway /chat both returned usable pages on recheck. Earlier health request also timed out. This is intermittent upstream availability, not a proven permanent fix. Link now goes straight to /chat; gateway renders bilingual guidance for ordinary navigation 429/5xx while preserving error status. API errors and security challenges pass through unchanged. No automatic retries, data migration or protection removal.
- No permanent availability guarantee: Render administration still requires working authorization to diagnose upstream limits; school Wi-Fi has not been tested here.
