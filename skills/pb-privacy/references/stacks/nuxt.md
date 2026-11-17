# Nuxt (Vue)

Where personal data leaks or gets collected in a Nuxt 3+ app.

## Consent before trackers (law.md section 2)
- Load analytics, ads, and social scripts through `@nuxt/scripts` with a consent trigger: `useScriptTriggerConsent()` passed as the script's `trigger`, and call its `accept()` when the user opts in. A script tag in `app.head` or an unconditional plugin runs before consent.
- Store the choice in a cookie read with `useCookie`, so the server render already knows it and no tracker is rendered for a user who refused. Send the choice to the API as well; the cookie alone is not proof of consent.

## Data sent to the browser (law.md section 1)
- Everything returned by `useFetch`, `useAsyncData`, and `useState` on the server is serialized into the page HTML, including fields the template never shows. Fetch only the fields needed: the `pick` option, or a narrower API response.
- `runtimeConfig.public` is visible to every visitor.

## URLs (law.md section 5)
- Keep emails, names, phone numbers, and tokens out of route params and query strings: URLs end up in analytics, server logs, browser history, and the `Referer` header. Set a `Referrer-Policy` (the `nuxt-security` module does).

## Third-party resources (law.md section 5)
- Self-host fonts with `@nuxt/fonts`; a font loaded from a third-party CDN sends each visitor's IP address to it.
- Embeds (video, maps, chat) load after a click or after consent, behind a static placeholder.
- Session-replay and analytics tools: mask form inputs, and do not pass names, emails, or user IDs as event properties.
