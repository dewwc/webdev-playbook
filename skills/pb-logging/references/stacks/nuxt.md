# Nuxt (Vue)

Two sides: the browser (frontend errors), and the Nitro server (`server/`), which is a backend and follows the same patterns as any API.

## Frontend errors

- Use an error tracker. For Sentry, the `@sentry/nuxt` module covers client and server. Set the release and environment, and turn on source map upload so stack traces are readable.
- Without a tracker, add a plugin that catches errors in one place:

```ts
// plugins/error-report.client.ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.config.errorHandler = (err, _instance, info) => {
    // send to your collector endpoint; include route and the last API traceId if known
    report({ message: String(err), stack: (err as Error)?.stack, info, route: useRoute().fullPath });
  };
  nuxtApp.hook('app:error', (err) => report({ message: String(err), stack: err?.stack }));
});
```

- Failed API calls: in a shared `$fetch` / `useFetch` wrapper (`onResponseError`), report status, URL, and the trace ID from the response header or the problem+json body. Show the trace ID to the user on error pages so they can report it.
- Never send tokens, form values, or personal data in reports.

## Nitro server (`server/api`, `server/routes`)

- Log JSON to stdout with a structured logger (e.g. pino). `consola` (Nuxt default) is fine for development, but configure JSON output for production.
- Central error logging: a Nitro plugin with the `error` hook logs each unhandled server error once:

```ts
// server/plugins/errors.ts
export default defineNitroPlugin((nitro) => {
  nitro.hooks.hook('error', (error, { event }) => {
    logger.error({ err: error, 'http.route': event?.path }, 'unhandled server error');
  });
});
```

- Errors returned with `createError` must not include stacks or internal messages in production.
