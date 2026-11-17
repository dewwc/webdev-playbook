# ASP.NET Core (.NET)

The server's share of Core Web Vitals is time to first byte (part of LCP) and how responses are compressed and cached. Check `Program.cs` for what is already set up.

## Time to first byte (LCP)
- Slow endpoints behind the first viewport are covered by `pb-code-quality`, if installed: blocking calls, queries in loops, unbounded reads, missing indexes. Without it, check for `.Result` / `.Wait()`, and for read queries without `AsNoTracking()`, a `Select` projection, and pagination.
- Return a DTO with the fields the page needs, not the whole entity. Smaller JSON is faster to send and to parse.

## Compression (delivery)
- Compress at the reverse proxy or CDN when there is one (nginx, IIS, Cloudflare). It is faster than doing it in the app.
- Otherwise: `AddResponseCompression(o => o.EnableForHttps = true)` with `UseResponseCompression()` (Brotli and gzip). HTTPS compression is off by default because compressing a response that mixes a secret with user-controlled text enables the BREACH attack; keep it off for such responses.

## Caching (delivery)
- Public, shared responses: output caching (.NET 7+), `AddOutputCache()` + `UseOutputCache()` + `.CacheOutput()` or `[OutputCache]`. By default it skips authenticated requests and responses that set a cookie; keep those defaults.
- Browser and CDN caching: `[ResponseCache(Duration = 60)]` sets `Cache-Control`. Per-user or sensitive responses: `[ResponseCache(NoStore = true, Location = ResponseCacheLocation.None)]`.
- Static files served by the app: .NET 9+ `MapStaticAssets()` fingerprints and pre-compresses them. With `UseStaticFiles`, set `Cache-Control: public,max-age=31536000,immutable` in `OnPrepareResponse`, for fingerprinted files only.

## Cross-origin API calls (LCP, INP)
- When the browser calls the API on another origin, each non-simple request is preceded by a preflight. Cache it: `policy.SetPreflightMaxAge(TimeSpan.FromHours(1))`.

## Protocol (delivery)
- Kestrel serves HTTP/2 over TLS by default. HTTP/3 is opt-in: `listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3`. Behind a proxy, the proxy's protocol is what the browser gets.
