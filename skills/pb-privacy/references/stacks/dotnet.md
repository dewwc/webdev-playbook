# ASP.NET Core (.NET)

Built-in features that meet the obligations in `law.md`. Check `Program.cs` and the Identity setup for what is already used.

## Cookie consent (law.md section 2)
- `Configure<CookiePolicyOptions>(o => o.CheckConsentNeeded = _ => true)` with `app.UseCookiePolicy()`: cookies not marked `IsEssential` are not written until `ITrackingConsentFeature.GrantConsent()` is called. Mark only cookies the service needs (auth, CSRF) as essential.
- Store a consent record in the database as well (user or visitor ID, purpose, wording version, timestamp); the consent cookie alone is not proof.

## Access, export, and deletion (law.md section 3)
- ASP.NET Core Identity: mark personal properties of the user class with `[PersonalData]`. The Identity UI's download and delete pages use that attribute; a custom API should cover the same properties.
- Personal data in other tables (orders, addresses, uploads, audit rows) is not covered by Identity: include each in the export and the delete.
- A soft delete with a global query filter (`HasQueryFilter(x => !x.IsDeleted)`) hides the row but keeps the personal data. Erasure needs a real delete or overwriting the personal fields.
- Check cascade delete behaviour for related tables, so no personal data is orphaned.

## Retention (law.md section 4)
- A `BackgroundService` with `PeriodicTimer` (or Hangfire / Quartz, if the project has one) that removes expired rows with `ExecuteDeleteAsync`, or anonymises them with `ExecuteUpdateAsync`.

## Protection and logs (law.md sections 4 and 6)
- Sensitive fields: encrypt per field with the Data Protection API (`IDataProtector`), with keys persisted outside the container. Identity can encrypt `[ProtectedPersonalData]` properties when `Stores.ProtectPersonalData` is on and an `ILookupProtector` is registered.
- Keep personal data out of logs with the logger's redaction (`Microsoft.Extensions.Compliance.Redaction`); log rules are in `pb-logging`, if installed.

## Sharing (law.md section 5)
- Send third parties a DTO with the fields they need, never the entity.
