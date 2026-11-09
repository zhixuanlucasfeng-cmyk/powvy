# Powvy website assistant

Public, bilingual website chat. The UI uses the site's manga theme and lives in `assets/chat.js` / `assets/chat.css`. The Worker uses Cloudflare Workers AI; there is no provider token in the browser.

## Deploy

Run `npm install`, `npm run test:chat`, then `npm run deploy:chat` with the owner's Cloudflare login. Schema: `npx wrangler d1 execute powvy-site-chat --remote --config chat-api/wrangler.jsonc --file chat-api/schema.sql`. Publish the static site through its usual GitHub Pages deployment.

`public-facts.json` contains only facts selected from the public homepage. Review and update it when projects change, then redeploy. Never import private chats or local notes. Replies are AI-generated and can still be inaccurate; this assistant has no action tools.

## Limits and privacy

- 1,200 characters per message, 8 messages / 5,000 characters per request, 16 KB request body.
- 12 attempts per IP per hour and 60 AI requests globally per UTC day, atomically enforced in D1, including requests from spoofed origins. These are initial conservative usage limits; failures after reservation count too.
- D1 stores expiring usage counters, not messages. IP-derived keys rotate daily and expire. Cloudflare processes inference content. Application request logging is disabled.
- Chat history exists only in page memory; clearing/reloading removes it. No automatic forwarding, mailbox, CRM or human inbox was created. Visitors can explicitly open the existing public WhatsApp contact.
- Provider failure, timeout or exhausted limits show a retry/human-contact state; no fabricated offline replies.

## Verify

`npm run test:chat` tests input boundaries, role restrictions, provider errors and concurrent quota enforcement with in-memory SQLite. For UI tests run a local static server at port 8778 and `npm run test:chat-ui` (installed Chrome required). UI tests mock AI responses and cover Chinese/English, safe text rendering, errors, clearing, dismissal and desktop/mobile layout. Real inference must be checked separately after Worker deployment.
