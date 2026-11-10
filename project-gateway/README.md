# Project entry gateway

`jc.powvy.org` forwards to the existing public JC deployment. It does not store data or grant admin access. Deploy with:

```sh
npx wrangler deploy --config project-gateway/wrangler.jsonc --env jc
node --test tests/project-gateway.test.mjs
```

Cloudflare manages the custom domain's DNS and certificate. Upstreams are fixed by configuration, never supplied by visitors. Authentication cookies and response streams are forwarded; only same-upstream Location redirects are rewritten. Exact same-origin requests have their Origin translated for Vercel's host handling; foreign/null origins are unchanged. Do not broaden that check.

The `solar` environment serves `solar-agent.powvy.org` from the current Cameroon backend, `rest-solar-agent-cm.onrender.com`. Deploy with the same command using `--env solar`. On 10 Nov 2026 the upstream challenge cleared and the real chat API returned a product-information reply; no verification protections were disabled. The old `rest-solar-agent.onrender.com` entry still timed out. Render CLI reauthorization remains unconfirmed; no Render service or database settings were changed.

Rest Solar remains on Render Free by owner choice. Its upstream response-header timeout is 90 seconds (JC stays at 45 seconds), allowing more room for Render cold starts. This is a bounded wait, not a keep-alive job or automatic replay of chat submissions. Render health checking uses `/health`. Free-tier sleep, edge challenges and rate limits still apply.
