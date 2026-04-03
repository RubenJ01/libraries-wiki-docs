Use `readableDate()` to turn a `DateTimeInterface` into a human-readable date string.

## Default Locale (`en`)

If you do not pass a locale, English is used by default.

```php
<?php

use DateTimeImmutable;

$date = new DateTimeImmutable('2026-03-30');

echo $humanizer->readableDate($date); // Monday 30 March 2026
```

## Explicit Locale

Pass a locale to format using a supported language.

```php
<?php

use DateTimeImmutable;

$date = new DateTimeImmutable('2026-03-30');

echo $humanizer->readableDate($date, Humanizer::LOCALE_NL); // Maandag 30 maart 2026
echo $humanizer->readableDate($date, 'nl_NL');              // Maandag 30 maart 2026
```

## Unsupported Locales

Unsupported locales fall back to English output.

```php
<?php

use DateTimeImmutable;

$date = new DateTimeImmutable('2026-03-30');

echo $humanizer->readableDate($date, 'fr'); // Monday 30 March 2026
```


