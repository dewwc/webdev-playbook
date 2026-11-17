# Core Web Vitals patterns

Thresholds are Google's, assessed at the 75th percentile of page loads, mobile and desktop separately.

| Metric | Measures | Good | Poor |
|---|---|---|---|
| LCP, Largest Contentful Paint | When the largest image or text block in the first viewport is painted | ≤ 2.5 s | > 4.0 s |
| INP, Interaction to Next Paint | Delay from a click, tap, or key press to the next paint; the slowest interaction of the visit, ignoring one outlier per 50 | ≤ 200 ms | > 500 ms |
| CLS, Cumulative Layout Shift | How much visible content moves without the user causing it | ≤ 0.1 | > 0.25 |

The last column of each table is the Lighthouse audit ID to cite.

## 1. LCP

LCP time = time to first byte + resource load delay + resource load duration + element render delay (`lcp-breakdown-insight`).

| Cause | Pattern | Audit |
|---|---|---|
| LCP image found late | The LCP image is an `<img>` in the server-rendered HTML (or has `<link rel="preload" as="image">`), with `fetchpriority="high"` and without `loading="lazy"`. It is not a CSS `background-image` and is not inserted by JavaScript. | `lcp-discovery-insight` |
| First-viewport content rendered on the client | Content of the first viewport is in the server response (SSR or prerender), not fetched after hydration. Where it must render on the client, it does not wait behind a login check or SDK start-up, and the calls it needs start together, not one after another. | `lcp-breakdown-insight` |
| Slow document | HTML that is the same for every user is prerendered or cached. The URL is reached without a redirect chain. Text compression is on. | `document-latency-insight` |
| Render-blocking requests | Scripts in `<head>` use `defer`, `async`, or `type="module"`. CSS that the first viewport does not need loads separately. No `@import` in the CSS the browser receives; one that the build resolves (Tailwind, Sass) is fine. | `render-blocking-insight` |
| Heavy image | AVIF or WebP, sized to the rendered size with `srcset` and `sizes`. | `image-delivery-insight` |
| Late connections and request chains | `<link rel="preconnect">` for the few origins the first viewport needs, the API origin included; none for an origin that waits for consent. No chain such as CSS → second CSS → font. | `network-dependency-tree-insight` |
| Font delays text | `font-display: swap` or `optional`. Fonts are self-hosted WOFF2, and the one or two used in the first viewport are preloaded. | `font-display-insight` (covers `font-display` only) |

## 2. CLS

A shift within 500 ms of a user interaction does not count.

| Cause | Pattern | Audit |
|---|---|---|
| Media without reserved space | `width` and `height` attributes (or CSS `aspect-ratio`) on every `<img>`, `<video>`, and `<iframe>`. | `unsized-images` |
| Late content pushes the page down | Space is reserved (`min-height`, or a skeleton of the final size) for ads, embeds, banners, and data that arrives later. New content is added below the viewport or in response to a user action. | `cls-culprits-insight` |
| Font swap changes text size | The fallback font has matched metrics (`size-adjust`, `ascent-override`), or `font-display: optional`. | `cls-culprits-insight` |
| Animation moves layout | Animate `transform` and `opacity`. Animating `top`, `left`, `width`, `height`, or `margin` is a finding when it moves other content; a bar that grows inside a fixed track moves nothing. | `non-composited-animations` (CSS animations), `cls-culprits-insight` (changes made by script) |

## 3. INP

INP = input delay + processing duration + presentation delay (`inp-breakdown-insight`).

| Cause | Pattern | Audit |
|---|---|---|
| Long tasks block input | No task over 50 ms: split the work and yield between parts (`await scheduler.yield()`, with a `setTimeout` fallback), or move it to a Web Worker. | `long-tasks` |
| Too much JavaScript | Code is split per route. Components behind an interaction (modal, editor, chart, map) load with dynamic `import()`. No unused dependencies, no library bundled twice, no polyfills for browsers the project does not support. | `unused-javascript`, `duplicated-javascript-insight`, `legacy-javascript-insight`, `bootup-time` |
| Handler finishes everything before the paint | The handler updates the UI first; non-visual work (analytics, saving) runs after the next paint. Expensive work in an `input` handler (search, validation, a network call) is debounced; a cheap visual update is not. | `inp-breakdown-insight` |
| Scroll, touch, and resize work | `scroll`, `resize`, `touchmove`, and `wheel` listeners are throttled (`requestAnimationFrame`) and `passive`; where a gesture must block scrolling, use CSS `touch-action`. They are not INP interactions, but their work delays the ones that are. | `long-tasks` |
| Leaked listeners | Listeners and timers a component adds are removed when it unmounts. | — |
| Layout thrashing | Layout reads (`offsetWidth`, `getBoundingClientRect()`) are batched before writes, never alternated in a loop. | `forced-reflow-insight` |
| Large DOM | Long lists and tables are virtualized or paginated. Off-screen sections use `content-visibility: auto`. | `dom-size-insight` |
| Third-party scripts | Loaded with `async` or `defer`. A script that tracks users loads after consent (`pb-privacy`, if installed); any other loads after first interaction where possible. Heavy embeds (video, chat, map) start as a static facade. | `third-parties-insight` |

## 4. Delivery and caching

Cache header semantics follow RFC 9111.

| Topic | Pattern | Audit |
|---|---|---|
| Static assets | Fingerprinted file names with `Cache-Control: public, max-age=31536000, immutable`. | `cache-insight` |
| HTML and API responses | Public pages: `Cache-Control: no-cache` (revalidate with `ETag`), or a short `s-maxage` with `stale-while-revalidate`. Per-user responses: `no-store` when they hold personal or sensitive data, otherwise `private`. | — |
| Compression | Brotli or gzip for HTML, CSS, JS, JSON, SVG. | `document-latency-insight` (the HTML document only) |
| Protocol | HTTP/2 or HTTP/3. | `modern-http-insight` |
| Page weight | Minified CSS and JS; no asset larger than its use needs. | `total-byte-weight`, `unminified-css`, `unminified-javascript`, `unused-css-rules` |
| Back/forward cache | No `unload` listeners (use `pagehide`). `no-store` only on pages with sensitive data. | `bf-cache` |
| Mobile viewport | `<meta name="viewport" content="width=device-width, initial-scale=1">`. | `viewport-insight` |

## References

- Web Vitals (thresholds): https://web.dev/articles/vitals
- Optimize LCP: https://web.dev/articles/optimize-lcp
- Optimize CLS: https://web.dev/articles/optimize-cls
- Optimize INP: https://web.dev/articles/optimize-inp
- RFC 9111 HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111
