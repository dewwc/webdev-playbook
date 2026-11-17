# Nuxt (Vue)

Where personal data leaks or gets collected in a Nuxt 3+ app.

## Consent before trackers (law.md section 2)
- Load analytics, ads, and social scripts through `@nuxt/scripts` with a consent trigger: `useScriptTriggerConsent()` passed as the script's `trigger`, and call its `accept()` when the user opts in. A script tag in `app.head` or an unconditional plugin runs before consent.
- An npm SDK can carry its own tracker (login, chat, and map SDKs do). Check what the imported package sends, and import only the modules the code uses when the SDK offers per-module imports.
- Store the choice in a cookie read with `useCookie`, so the server render already knows it and no tracker is rendered for a user who refused. Send the choice to the API as well; the cookie alone is not proof of consent.

## Data sent to the browser (law.md section 1)
- Everything returned by `useFetch`, `useAsyncData`, and `useState` on the server is serialized into the page HTML, including fields the template never shows. Fetch only the fields needed: the `pick` option, or a narrower API response.
- `runtimeConfig.public` is visible to every visitor.
- `localStorage` and `sessionStorage` are stores: list what they hold in the inventory, keep personal data out of them where a server call would do, and clear them on logout.

## URLs (law.md section 5)
- Keep emails, names, phone numbers, and tokens out of route params and query strings: URLs end up in analytics, server logs, and browser history. Browsers send only the origin to other sites by default (`strict-origin-when-cross-origin`); never set a weaker `Referrer-Policy`.

## Third-party resources (law.md section 5)
- Self-host fonts with `@nuxt/fonts`; a font loaded from a third-party CDN sends each visitor's IP address to it.
- Embeds (video, maps, chat) load after a click or after consent, behind a static placeholder.
- Session-replay and analytics tools: mask form inputs, and do not pass names, emails, or user IDs as event properties.
