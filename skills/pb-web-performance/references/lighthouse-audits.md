# Lighthouse performance audits

Source: Lighthouse 13.6.0 (Apache-2.0). Cite as the audit ID, e.g. `lcp-discovery-insight`.
Each line is the audit's own description. Follow its link for how to fix.

## Metrics (weight = share of the performance score)

- **first-contentful-paint** (weight 10) — First Contentful Paint marks the time at which the first text or image is painted. [Learn more about the First Contentful Paint metric](https://developer.chrome.com/docs/lighthouse/performance/first-contentful-paint/).
- **largest-contentful-paint** (weight 25) — Largest Contentful Paint marks the time at which the largest text or image is painted. [Learn more about the Largest Contentful Paint metric](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-largest-contentful-paint/)
- **total-blocking-time** (weight 30) — Sum of all time periods between FCP and Time to Interactive, when task length exceeded 50ms, expressed in milliseconds. [Learn more about the Total Blocking Time metric](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time/).
- **cumulative-layout-shift** (weight 25) — Cumulative Layout Shift measures the movement of visible elements within the viewport. [Learn more about the Cumulative Layout Shift metric](https://web.dev/articles/cls).
- **speed-index** (weight 10) — Speed Index shows how quickly the contents of a page are visibly populated. [Learn more about the Speed Index metric](https://developer.chrome.com/docs/lighthouse/performance/speed-index/).

## Insights

- **cache-insight** — A long cache lifetime can speed up repeat visits to your page. [Learn more about caching](https://developer.chrome.com/docs/performance/insights/cache).
- **cls-culprits-insight** — Layout shifts occur when elements move absent any user interaction. [Investigate the causes of layout shifts](https://developer.chrome.com/docs/performance/insights/cls-culprit), such as elements being added, removed, or their fonts changing as the page loads.
- **document-latency-insight** — Your first network request is the most important. [Reduce its latency](https://developer.chrome.com/docs/performance/insights/document-latency) by avoiding redirects, ensuring a fast server response, and enabling text compression.
- **dom-size-insight** — A large DOM can increase the duration of style calculations and layout reflows, impacting page responsiveness. A large DOM will also increase memory usage. [Learn how to avoid an excessive DOM size](https://developer.chrome.com/docs/performance/insights/dom-size).
- **duplicated-javascript-insight** — Remove large, [duplicate JavaScript modules](https://developer.chrome.com/docs/performance/insights/duplicated-javascript) from bundles to reduce unnecessary bytes consumed by network activity
- **font-display-insight** — Consider setting [font-display](https://developer.chrome.com/docs/performance/insights/font-display) to swap or optional to ensure text is consistently visible. swap can be further optimized to mitigate layout shifts with [font metric overrides](https://developer.chrome.com/blog/font-fallbacks).
- **forced-reflow-insight** — A forced reflow occurs when JavaScript queries geometric properties (such as offsetWidth) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about [forced reflows](https://developer.chrome.com/docs/performance/insights/forced-reflow) and possible mitigations.
- **image-delivery-insight** — Reducing the download time of images can improve the perceived load time of the page and LCP. [Learn more about optimizing image size](https://developer.chrome.com/docs/performance/insights/image-delivery).
- **inp-breakdown-insight** — Start investigating [how to improve INP](https://developer.chrome.com/docs/performance/insights/inp-breakdown) by looking at the longest subpart
- **lcp-breakdown-insight** — Each [subpart has specific improvement strategies](https://developer.chrome.com/docs/performance/insights/lcp-breakdown). Ideally, most of the LCP time should be spent on loading the resources, not within delays.
- **lcp-discovery-insight** — [Optimize LCP](https://developer.chrome.com/docs/performance/insights/lcp-discovery) by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
- **legacy-javascript-insight** — Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren’t necessary for modern browsers. Consider modifying your JavaScript build process to not transpile [Baseline](https://web.dev/articles/baseline-and-polyfills) features, unless you know you must support older browsers. [Learn why most sites can deploy ES6+ code without transpiling](https://developer.chrome.com/docs/performance/insights/legacy-javascript).
- **modern-http-insight** — HTTP/2 and HTTP/3 offer many benefits over HTTP/1.1, such as multiplexing. [Learn more about using modern HTTP](https://developer.chrome.com/docs/performance/insights/modern-http).
- **network-dependency-tree-insight** — [Avoid chaining critical requests](https://developer.chrome.com/docs/performance/insights/network-dependency-tree) by reducing the length of chains, reducing the download size of resources, or deferring the download of unnecessary resources to improve page load
- **render-blocking-insight** — Requests are blocking the page’s initial render, which may delay LCP. [Deferring or inlining](https://developer.chrome.com/docs/performance/insights/render-blocking) can move these network requests out of the critical path.
- **third-parties-insight** — 3rd party code can significantly impact load performance. [Reduce and defer loading of 3rd party code](https://developer.chrome.com/docs/performance/insights/third-parties) to prioritize your page’s content.
- **viewport-insight** — Tap interactions may be [delayed by up to 300 ms](https://developer.chrome.com/docs/performance/insights/viewport) if the viewport isn’t optimized for mobile

## Diagnostics

- **unminified-css** — Minifying CSS files can reduce network payload sizes. [Learn how to minify CSS](https://developer.chrome.com/docs/lighthouse/performance/unminified-css/).
- **unminified-javascript** — Minifying JavaScript files can reduce payload sizes and script parse time. [Learn how to minify JavaScript](https://developer.chrome.com/docs/lighthouse/performance/unminified-javascript/).
- **unused-css-rules** — Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. [Learn how to reduce unused CSS](https://developer.chrome.com/docs/lighthouse/performance/unused-css-rules/).
- **unused-javascript** — Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. [Learn how to reduce unused JavaScript](https://developer.chrome.com/docs/lighthouse/performance/unused-javascript/).
- **total-byte-weight** — Large network payloads cost users real money and are highly correlated with long load times. [Learn how to reduce payload sizes](https://developer.chrome.com/docs/lighthouse/performance/total-byte-weight/).
- **user-timings** — Consider instrumenting your app with the User Timing API to measure your app's real-world performance during key user experiences. [Learn more about User Timing marks](https://developer.chrome.com/docs/lighthouse/performance/user-timings/).
- **bootup-time** — Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. [Learn how to reduce Javascript execution time](https://developer.chrome.com/docs/lighthouse/performance/bootup-time/).
- **mainthread-work-breakdown** — Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. [Learn how to minimize main-thread work](https://developer.chrome.com/docs/lighthouse/performance/mainthread-work-breakdown/)
- **long-tasks** — Lists the longest tasks on the main thread, useful for identifying worst contributors to input delay. [Learn how to avoid long main-thread tasks](https://web.dev/articles/optimize-long-tasks)
- **non-composited-animations** — Animations which are not composited can be janky and increase CLS. [Learn how to avoid non-composited animations](https://developer.chrome.com/docs/lighthouse/performance/non-composited-animations/)
- **unsized-images** — Set an explicit width and height on image elements to reduce layout shifts and improve CLS. [Learn how to set image dimensions](https://web.dev/articles/optimize-cls#images_without_dimensions)
- **bf-cache** — Many navigations are performed by going back to a previous page, or forwards again. The back/forward cache (bfcache) can speed up these return navigations. [Learn more about the bfcache](https://developer.chrome.com/docs/lighthouse/performance/bf-cache/)
