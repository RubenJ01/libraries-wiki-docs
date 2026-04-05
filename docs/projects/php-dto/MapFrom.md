Use `#[MapFrom('path')]` on a constructor parameter to read a value from a different key path. Paths use **dot notation** for nested arrays.

## Examples

```php
<?php

#[MapFrom('profile.first_name')]
public readonly string $firstName
```

```php
<?php

#[MapFrom('stats.play_count')]
public readonly int $playCount
```

If the path does not exist in the source data, the value is treated as missing (and defaults apply when available).

## Next

- [Home](index.md)
- [CastTo](CastTo.md)
