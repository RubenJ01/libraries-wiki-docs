## Factory

```php
<?php

use Rjds\PhpSlugify\SluggerFactory;

$slugger = SluggerFactory::create();
```

## Basic

```php
<?php

echo $slugger->slugify('Hello World 2026!');
```

Outputs: `hello-world-2026`

## Divider

Default is `-`. Use another character as the second argument:

```php
<?php

echo $slugger->slugify('Hello World 2026', '_');
```

Outputs: `hello_world_2026`

## Custom mappings

Applied before transliteration. Named argument `mappings`:

```php
<?php

echo $slugger->slugify('Tom & Jerry', mappings: ['&' => 'and']);
echo $slugger->slugify('contact@example.com', mappings: ['@' => ' at ', '.' => ' dot ']);
echo $slugger->slugify('Price 10€', divider: '_', mappings: ['€' => ' eur']);
```

User mappings override locale rules when they target the same character (see [Locales](Locales.md)).

## Max length

Truncation prefers word boundaries:

```php
<?php

echo $slugger->slugify('The Quick Brown Fox', maxLength: 14);
echo $slugger->slugify('Hello World', maxLength: 50);
echo $slugger->slugify('Hello World 2026', '_', maxLength: 15);
```

## Empty input

Default: empty string in → empty string out.

```php
<?php

echo $slugger->slugify('');
echo $slugger->slugify('', emptyValue: 'n-a');
```

## Next

- [Home](index.md)
- [Locales](Locales.md)
- [Installation](Installation.md)
