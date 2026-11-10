# JC and A-Level connection investigation — 2026-11-10

Reported context: desktop Chrome on school Wi-Fi, blank page after clicking a project. The exact URL visible during failure has not yet been supplied.

Observed from the current execution network (not proof of the friend's exact failure):
- powvy.org: HTTP 200, TCP/TLS completed.
- dryruncs.com: HTTP 200, TCP/TLS completed (also on Vercel).
- vercel.com: HTTP 200.
- jc-sports-day-scoring.vercel.app and alevel-survival-bureau.vercel.app: TCP connection to port 443 timed out before TLS or HTTP.
- Tested both local DNS addresses and addresses returned by Google public DNS. All eight address/hostname combinations timed out. No DNS settings were changed.
- Vercel CLI inspected both production deployments: Ready, aliases mapped to the intended deployments. The Vercel status page reported operational. Neither alone proves application health.
- Browser checks could not reach DOMContentLoaded, including scripts-blocked and JavaScript-disabled variants. Therefore these runs cannot diagnose app rendering or reproduce the exact visual symptom.
- Previous-day Chrome and WebKit checks did load both apps and their inner routes.

No evidence yet distinguishes network filtering, routing failure, or another network-path problem. Rebuilding app code is not a justified fix for a failure before TCP connection. No claim that the school caused the failure, and no claim that the blank-page issue has been fixed.

Added connection.html and a help link in both project detail views. The page probes the same-origin homepage and the two public app URLs using credential-free HEAD requests. Cross-origin responses are opaque: response receipt is explicitly NOT labeled app success and could be a filter page. Failures and 12-second timeouts remain visible. No automatic telemetry; reports are copied only by user action. Static direct links and instructions work without JavaScript. Study data is not read or erased.

Verification: tests/connection-ui.mjs covers response/failure/timeout distinction, no-JS instructions, mobile layout and project help link. Need a report from the affected school computer, full blank-page URL, and Console errors if HTTP is reachable. If network filtering is confirmed, school IT must review the two domains and their DNS/HTTPS/filter logs.
