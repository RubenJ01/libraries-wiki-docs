Use `#[ArrayOf(SomeDto::class)]` on an `array` constructor parameter to map each **list item** to an instance of `SomeDto` via `DtoMapper`.

## Requirements

- The source value must be an array of **associative arrays** (one per item).
- Each element is passed to `DtoMapper::map()` for the given class. If an element is not an array, mapping throws `InvalidArgumentException`.

## Example

```php
<?php

/** @param list<TagDto> $tags */
public function __construct(
    #[ArrayOf(TagDto::class)]
    public readonly array $tags,
) {
}
```

## Next

- [Home](index.md)
- [DtoMapper](DtoMapper.md)
