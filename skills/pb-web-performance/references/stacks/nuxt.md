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

## SPA mode, `ssr: false` (LCP)
The rules above assume server rendering. With `ssr: false` the server response has no content, so LCP waits for the bundle and every call after it.
- Give the first paint something: `app/spa-loading-template.html`. A prerendered page has content only when it is server-rendered, so for pages that are the same for every user keep `ssr: true` and switch it off per route instead (`routeRules: { '/app/**': { ssr: false } }`).
- Render `<NuxtPage>` at once. Keep it out of a `v-if` that waits for a login check or SDK start-up; let the page start its own data call in parallel with them.

## JavaScript (INP)
- Give components that are behind an interaction or below the first viewport, and are large or import a heavy dependency, the `Lazy` prefix (`<LazyChatWidget v-if="open" />`); Nuxt splits them into their own chunk.
- Import only the parts of an SDK the code uses, when the SDK offers per-module imports.
- Nuxt 3.16+: delay hydration of lazy components with `hydrate-on-visible`, `hydrate-on-interaction`, or `hydrate-on-idle`.
- Load third-party scripts with `@nuxt/scripts` (`useScript` with a `trigger`) instead of script tags in `app.head`.
- Check bundle contents with `npx nuxi analyze`.

## Fonts (LCP, CLS)
- `@nuxt/fonts` self-hosts fonts. It generates a fallback with matched metrics for the first family of each `font-family` declaration only, so put the font most of the text uses first. For a non-Latin script (Thai), check the generated `@font-face` rules: the fallback is built from Latin system fonts.
- It preloads a font by default only when the font has no `subsets`. For a subsetted font used in the first viewport, set `preload: true` on that family.

## Layout stability (CLS)
- `<ClientOnly>` renders nothing on the server: give it a `#fallback` slot with the final size.

## Caching (delivery)
- Set `routeRules` per route: `prerender: true` for static pages, `swr` or `isr` for public pages that change. Pages that depend on the logged-in user get no cache rule.
