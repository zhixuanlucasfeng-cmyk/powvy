# Project entry gateway

`jc.powvy.org` forwards to the existing public JC deployment. It does not store data or grant admin access. Deploy with:

```sh
npx wrangler deploy --config project-gateway/wrangler.jsonc --env jc
node --test tests/project-gateway.test.mjs
```

Cloudflare manages the custom domain's DNS and certificate. Upstreams are fixed by configuration, never supplied by visitors. Authentication cookies and response streams are forwarded; only same-upstream Location redirects are rewritten. Exact same-origin requests have their Origin translated for Vercel's host handling; foreign/null origins are unchanged. Do not broaden that check.

The `solar` environment serves `solar-agent.powvy.org` directly from the Cloudflare Python Durable Object `rest-solar-production` (class `SolarRuntime`). `/static/*` uses Workers Assets. API responses, streaming AI replies, and WebSocket upgrades pass through unchanged; the Solar branch never calls Render. JC keeps its existing proxy behavior.

Before deploying Solar, prepare assets from the matching Rest Solar checkout:

```sh
mkdir -p project-gateway/solar-assets
ln -s /absolute/path/to/rest-solar-agent/static project-gateway/solar-assets/static
node --test tests/project-gateway.test.mjs
npx wrangler deploy --config project-gateway/wrangler.jsonc --env solar
```

The asset directory is ignored by Git. Deploy the backend and `rest-solar-language` first using their repository's `cloudflare` configurations. The backend retains the original Neon PostgreSQL public schema and signing key; Hyperdrive caches no queries. Handoff state lives in Durable Object storage, with a one-time guarded import from the former Redis state. Do not put migration credentials in this public gateway.

The fixed object name `rest-solar-staging` is historical: the binding points to the separate production namespace, not the staging deployment. Do not change the name without migrating active handoff state.

No paid plan was enabled. Cloudflare free quotas and model-provider rate limits still apply. The previous Render service is retained for recovery, but switching back requires reconciling current handoff state into Redis first; PostgreSQL remains shared. Old proxy version: `7fd865a6-ec03-48f7-bce3-cffb4336ecae`. Do not blindly revert while customers are in live handoff sessions.
