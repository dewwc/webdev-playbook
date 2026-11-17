---
name: pb-web-performance
description: build and review web frontend code against core web vitals (lcp, inp, cls) and lighthouse performance audits. use when writing or reviewing pages, layouts, images, fonts, css or script loading, third-party scripts, bundles and code splitting, hydration, long lists, animations, http cache headers, or when asked why a page is slow or for a performance / page speed / lighthouse / core web vitals review or audit of a page, component, diff, or pr.
---

# Web performance (Core Web Vitals)

A page is fast enough when real users get **LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1** at the 75th percentile, on mobile and on desktop. Reading code cannot measure these numbers; it finds their causes. Treat the causes as part of "done" for any page or component.

## Workflow

1. Identify which metric the change can move (routing table below).
2. Load `references/core-web-vitals.md`. Detect the stack (`nuxt.config.*` → `nuxt.md`, `*.csproj` → `dotnet.md`) and load each match from `references/stacks/`; a Nuxt + .NET project loads both.
3. Write the code so it follows every pattern in the matching sections. Prefer framework built-ins (image component, lazy components, route cache rules) over hand-written loading code.
4. Before finishing, report which patterns were applied and which need a measurement to confirm, citing the metric and the Lighthouse audit ID, e.g. `LCP (lcp-discovery-insight)`.

## Routing table

Sections are in `references/core-web-vitals.md`.

| Change touches | Metric | Section |
|---|---|---|
| First-viewport image or heading, server response, redirects, CSS or scripts in `<head>`, fonts, data needed for the first viewport | LCP | 1 |
| Images, video, iframes, ads, embeds, banners, content inserted after load, web fonts, animations | CLS | 2 |
| Event handlers, heavy JavaScript, bundle size, hydration, long lists and tables, third-party scripts | INP | 3 |
| `Cache-Control`, compression, CDN, back/forward navigation, viewport meta | Delivery | 4 |

## Review mode

When asked to review a page, component, diff, or PR:

1. Load the files of Workflow step 2.
2. For each page in scope, name the likely LCP element from the markup: the largest image or text block in the first viewport. Put the list at the top of the report. Most LCP findings depend on it.
3. For a diff, check the sections the routing table maps the change to. For a whole page or project, check all four sections. In both cases check every rule in the loaded stack files.
4. Report only findings, one per broken pattern: `path:line — <LCP | CLS | INP | Delivery> (<audit-id>): <problem>. <fix>.` Leave the audit ID out when the pattern has none, as most stack-file rules do. For something missing, anchor the finding at the file where it belongs. Order by reach: the LCP element and code that runs on every page (layout, global scripts) first.
5. List separately what source code cannot show: whether the element of step 2 is the real LCP element, real interaction delay, layout shift on slow networks, and anything set outside the code (protocol and compression at the proxy, minification, unused or duplicated JavaScript in the built bundle, long tasks, back/forward cache).

If the page can be run, measure it: `npx lighthouse <url> --only-categories=performance --output=json --output-path=./lighthouse.json`. Load `references/lighthouse-audits.md` to read the report. State two limits with the result: a Lighthouse run is one lab device, while pass or fail is decided by field data (Chrome UX Report, or the `web-vitals` library in production); and a page-load run does not measure INP, so Total Blocking Time is its lab stand-in.

## Rules

- Security and privacy win over speed. Responses with personal or sensitive data keep `Cache-Control: no-store` and stay out of shared caches, even though that costs repeat-visit speed and can cost the back/forward cache. Never propose caching them. A missing `no-store` is a security finding (ASVS 14.2.2 and 14.3.2 in `pb-secure-coding`), not a performance finding: mention it in one line outside the findings list.
- A script that tracks users loads after consent, not merely after first interaction (`pb-privacy`, if installed).
- Lazy-load only what is below the first viewport or behind an interaction.
- An optimization that is not one of the listed patterns needs a measurement first: state the number before and after.
- If a pattern conflicts with the user's design instruction, follow the user but state the metric impact in one line.
