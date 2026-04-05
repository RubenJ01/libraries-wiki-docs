Map associative arrays to typed constructor DTOs using attributes. See the main repository [README](https://github.com/RubenJ01/php-dto#readme) for badges and CI.

## Start here

- [Installation](Installation.md)
- [DtoMapper](DtoMapper.md)
- [MapFrom](MapFrom.md)
- [CastTo](CastTo.md)
- [ArrayOf](ArrayOf.md)

## Quick example

```php
<?php

use Rjds\PhpDto\Attribute\ArrayOf;
use Rjds\PhpDto\Attribute\CastTo;
use Rjds\PhpDto\Attribute\MapFrom;
use Rjds\PhpDto\DtoMapper;

final class TagDto
{
    public function __construct(
        public readonly string $name,
        public readonly string $url,
    ) {
    }
}

final class ArtistDto
{
    /** @param list<TagDto> $tags */
    public function __construct(
        public readonly string $name,
        #[MapFrom('stats.play_count')]
        #[CastTo('int')]
        public readonly int $playCount,
        #[ArrayOf(TagDto::class)]
        public readonly array $tags,
    ) {
    }
}

$mapper = new DtoMapper();

$artist = $mapper->map([
    'name' => 'Arctic Monkeys',
    'stats' => ['play_count' => '150316'],
    'tags' => [
        ['name' => 'rock', 'url' => 'https://www.last.fm/tag/rock'],
    ],
], ArtistDto::class);
```

## Next steps

- For defaults when keys are missing, see [DtoMapper](DtoMapper.md).
- For nested keys and renames, see [MapFrom](MapFrom.md).
