# NestJS

Check `package.json` first. If the project already uses a logger (`nestjs-pino`, `winston`, `nest-winston`), keep it and apply the patterns to it.

## Setup (nestjs-pino)

`nestjs-pino` writes JSON with pino and logs one line per request through `pino-http`.

```ts
// app.module.ts
LoggerModule.forRoot({
  pinoHttp: {
    level: process.env.LOG_LEVEL ?? 'info',
    redact: ['req.headers.authorization', 'req.headers.cookie', 'res.headers["set-cookie"]'],
    customProps: () => ({ 'service.name': 'ev-api', 'deployment.environment': process.env.NODE_ENV }),
  },
}),

// main.ts
const app = await NestFactory.create(AppModule, { bufferLogs: true });
app.useLogger(app.get(Logger)); // Logger from 'nestjs-pino'
```

- In services, keep using Nest's `Logger` (`private readonly logger = new Logger(MyService.name)`). It is routed to pino.
- Structured fields: `this.logger.warn({ chargerId, durationMs }, 'ocpp call slow')`.

## Trace ID

- With OpenTelemetry (`@opentelemetry/sdk-node` + auto-instrumentations, including pino instrumentation), `trace_id` and `span_id` are added to pino logs automatically.
- Without OTel: set `pinoHttp.genReqId` to reuse an incoming `x-request-id` (or the trace ID from `traceparent`) or generate a UUID, and return it in a response header.

## Global exception filter

```ts
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger('Exceptions');
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const req = ctx.getRequest(); const res = ctx.getResponse();
    const status = exception instanceof HttpException ? exception.getStatus() : 500;
    if (status >= 500) this.logger.error(exception); // pino serializes type, message, stack
    res.status(status).type('application/problem+json').json({
      type: 'about:blank',
      title: status >= 500 ? 'Internal Server Error' : (exception as HttpException).message,
      status,
      traceId: req.id,
    });
  }
}
```

Register it once (`app.useGlobalFilters(...)` or an `APP_FILTER` provider). If a filter already exists, extend it rather than adding a second one.

## Jobs

`@nestjs/schedule` `@Cron` methods and queue processors (`@Processor`) are not covered by the HTTP filter. Wrap each run in try/catch that logs once, with job name and duration.
