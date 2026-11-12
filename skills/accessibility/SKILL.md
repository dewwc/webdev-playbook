---
name: accessibility
description: build and review web ui against wcag 2.2 accessibility success criteria (a/aa). use when writing or reviewing html, components, forms, modals, menus, tabs, tables, images, icons, video, color and contrast, focus and keyboard navigation, aria, error messages, or when asked for an accessibility / a11y review, audit, or wcag compliance check of a page, component, diff, or pr.
---

# Accessibility (WCAG 2.2)

Treat accessibility as part of "done" for any UI change. When writing UI, meet the applicable success criteria by default. When reviewing, check them and cite IDs.

## Workflow

1. Identify what the UI change contains (use the routing table below).
2. Load only the matching principle files from `references/wcag/`.
3. Target **Level AA** (includes A) unless the user specifies otherwise. AAA criteria are optional.
4. Build with native HTML first: `<button>`, `<a href>`, `<label>`, `<fieldset>`, `<table>`, headings in order, landmarks (`<main>`, `<nav>`). Add ARIA only when no native element fits. For custom widgets (combobox, tabs, dialog, menu, tree), follow the WAI-ARIA Authoring Practices pattern: https://www.w3.org/WAI/ARIA/apg/patterns/
5. Before finishing, check the result against the loaded criteria. Briefly report which ones were applied and any that need a manual check, citing `WCAG <num> (<level>)`.

For "how to meet" details of one criterion, open its *Understanding* link in the reference file.

## Routing table

Paths are relative to `references/`.

| UI contains | Load |
|---|---|
| Images, icons, SVG, video, audio, charts | `wcag/1-perceivable.md` (1.1, 1.2) |
| Page structure, headings, tables, lists, reading order, orientation | `wcag/1-perceivable.md` (1.3) |
| Color, contrast, text resize, zoom/reflow, spacing, hover/focus popups | `wcag/1-perceivable.md` (1.4) |
| Keyboard use, focus order, focus visibility, shortcuts, skip links | `wcag/2-operable.md` (2.1, 2.4) |
| Timeouts, auto-play, carousels, animation, flashing | `wcag/2-operable.md` (2.2, 2.3) |
| Page titles, link text, navigation, sticky headers covering focus | `wcag/2-operable.md` (2.4) |
| Touch targets, drag and drop, gestures, pointer cancel | `wcag/2-operable.md` (2.5) |
| Language, predictable behavior, consistent navigation and help | `wcag/3-understandable.md` (3.1, 3.2) |
| Forms, labels, validation errors, login/authentication, redundant entry | `wcag/3-understandable.md` (3.3) |
| Custom components, ARIA, name/role/value, status messages (toasts) | `wcag/4-robust.md` |

Common combinations:
- Form: 1-perceivable (1.3), 2-operable, 3-understandable, 4-robust
- Modal / dropdown / custom widget: 2-operable, 4-robust
- Content page: 1-perceivable, 2-operable (2.4)

## Review mode

When asked to review a page, component, diff, or PR:

1. Map the UI to rows in the routing table and load those files.
2. Check each applicable criterion at the target level.
3. Report only findings, one per line: `path:line — WCAG <num> (<level>): <problem>. <fix>.` Order by user impact (blocks a task > degrades it).
4. List criteria that need a running page or a human to verify (contrast of final colors, screen reader output, zoom at 400%) separately.

If the page can be run, suggest or run automated checks: `axe-core` (e.g. `@axe-core/playwright`) or Lighthouse accessibility. State that automated tools catch only part of WCAG issues; keyboard-only and screen reader checks are still needed.

## Rules

- Never remove the focus outline without a visible replacement.
- Every interactive element is reachable and operable by keyboard, and has an accessible name.
- Never use color alone to convey meaning (errors, status, required fields).
- Do not add ARIA that conflicts with native semantics (`role="button"` on `<button>`, `aria-hidden` on focusable elements).
- If a requirement conflicts with the user's design instruction, follow the user but state the accessibility impact in one line.
