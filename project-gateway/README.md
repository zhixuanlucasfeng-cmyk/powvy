# Project entry gateway

`jc.powvy.org` forwards to the existing public JC deployment. It does not store data or grant admin access. Deploy with:

```sh
npx wrangler deploy --config project-gateway/wrangler.jsonc --env jc
node --test tests/project-gateway.test.mjs
```

Cloudflare manages the custom domain's DNS and certificate. Upstreams are fixed by configuration, never supplied by visitors. Authentication cookies and response streams are forwarded; only same-upstream Location redirects are rewritten. Exact same-origin requests have their Origin translated for Vercel's host handling; foreign/null origins are unchanged. Do not broaden that check.

The `solar` environment is an unlinked diagnostic deployment. Its current Render upstream returns a Cloudflare challenge; it is NOT a verified working product. Restore owner Render access and inspect the service before publishing a custom domain or linking it from the website.
