Human-friendly formatting helpers for sizes, rates, numbers, dates, durations, lists, and more.

## Start here

- [Installation](Installation.md)
- [Numbers](Numbers.md) (also includes abbreviations, percentages, and words)
- [File Size](File-Size.md) / [Data Rate](Data-Rate.md)
- [Duration](Duration.md) / [Time Difference](Time-Difference.md)
- [Date Formatting](Date-Formatting.md)
- [Custom Formatters](Custom-Formatters.md)
- [Built-in Formatter Names](Built-in-Formatter-Names.md)

## Quick example

```php
<?php

use DateTimeImmutable;
use Rjds\PhpHumanize\Humanizer;

$h = new Humanizer();

echo $h->fileSize(1536); // "1.5 KB"
echo $h->dataRate(1048576); // "1 MB/s"
echo $h->ordinal(21); // "21st"
echo $h->duration(3661); // "1 hour, 1 minute, 1 second"
echo $h->diffForHumans(new DateTimeImmutable('-5 minutes')); // "5 minutes ago"
echo $h->readableDate(new DateTimeImmutable('2026-03-30')); // "Monday 30 March 2026"
echo $h->joinList(['A', 'B', 'C']); // "A, B, and C"
echo $h->truncate('The quick brown fox jumps over the lazy dog', 20); // "The quick brown fox…"
```

## What do you want to format?

- File sizes: [File Size](File-Size.md)
- Data rates: [Data Rate](Data-Rate.md)
- Ordinals: [Ordinals](Ordinals.md)
- Numbers: [Numbers](Numbers.md)
- Durations: [Duration](Duration.md)
- “x minutes ago”: [Time Difference](Time-Difference.md)
- Dates: [Date Formatting](Date-Formatting.md)
- Plurals: [Pluralization](Pluralization.md)
- Lists: [List Joining](List-Joining.md)
- Truncation: [Text Truncation](Text-Truncation.md)

## Next steps

- If you need project-wide defaults (locale, precision, list conjunction, truncation suffix), see the main repo `README.md`.
- If you want to override built-in formatters by key, use [Built-in Formatter Names](Built-in-Formatter-Names.md).

