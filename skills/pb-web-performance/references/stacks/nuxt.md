# Nuxt (Vue)

How to meet the Core Web Vitals patterns in Nuxt 3+.

## Images (LCP, CLS)
- Use `<NuxtImg>` / `<NuxtPicture>` from `@nuxt/image` with `width`, `height`, `sizes`, and `format="webp"` (or `avif`).
- LCP image: add `preload` and `fetchpriority="high"`, and leave `loading` at its default. Images below the first viewport: `loading="lazy"`.

## Data for the first viewport (LCP)
- Fetch with `useFetch` / `useAsyncData`, so the data renders on the server and is reused on hydration. A bare `$fetch` in `<script setup>` runs twice, once on the server and once in the browser.
- Ask for only the fields the page shows (`pick`, or a narrower API response): the result is embedded in the page HTML.
- On the server, call the API by its internal address, and start independent calls together (`Promise.all` inside `useAsyncData`).
- Use `lazy: true` or `server: false` only for content below the first viewport.

## JavaScript (INP)
- Give components behind an interaction or below the first viewport the `Lazy` prefix (`<LazyChatWidget v-if="open" />`); Nuxt splits them into their own chunk.
- Nuxt 3.16+: delay hydration of lazy components with `hydrate-on-visible`, `hydrate-on-interaction`, or `hydrate-on-idle`.
- Load third-party scripts with `@nuxt/scripts` (`useScript` with a `trigger`) instead of script tags in `app.head`.
- Check bundle contents with `npx nuxi analyze`.

## Fonts (LCP, CLS)
- `@nuxt/fonts` self-hosts fonts and generates fallback fonts with matched metrics.

## Layout stability (CLS)
- `<ClientOnly>` renders nothing on the server: give it a `#fallback` slot with the final size.

## Caching (delivery)
- Set `routeRules` per route: `prerender: true` for static pages, `swr` or `isr` for public pages that change. Pages that depend on the logged-in user get no cache rule.
