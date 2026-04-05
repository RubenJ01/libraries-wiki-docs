Use `#[CastTo('type')]` on a constructor parameter to convert the resolved scalar value before it is passed to the constructor.

## Supported types

| Type | Behavior |
| --- | --- |
| `int` | Cast to integer |
| `float` | Cast to float |
| `string` | Cast to string |
| `bool` | Strings `1` / `true` (case-insensitive) are true; other strings cast with `(bool)` |
| `datetime` | Builds a `DateTimeImmutable` with `setTimestamp((int) $value)` — input must be a **Unix timestamp** (integer or numeric string) |

Unsupported `CastTo` types throw `InvalidArgumentException`.

## Example

```php
<?php

#[CastTo('int')]
public readonly int $playCount

#[CastTo('datetime')]
public readonly \DateTimeImmutable $createdAt
```

## Next

- [Home](index.md)
- [ArrayOf](ArrayOf.md)
