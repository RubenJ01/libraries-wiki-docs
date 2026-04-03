URL-safe slugs from arbitrary strings: transliteration, locales, custom mappings, length limits, and configurable dividers.

## Start here

- [Installation](Installation.md)
- [Usage](Usage.md)
- [Locales](Locales.md)

## Quick example

```php
<?php

use Rjds\PhpSlugify\SluggerFactory;

$slugger = SluggerFactory::create();
echo $slugger->slugify('Hello World 2026!');
```

Outputs: `hello-world-2026`

Packagist: [`rjds/php-slugify`](https://packagist.org/packages/rjds/php-slugify) · Repo: [github.com/RubenJ01/php-slugify](https://github.com/RubenJ01/php-slugify)
