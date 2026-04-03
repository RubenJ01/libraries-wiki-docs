## Built-in locales

Pass a locale into the factory (not `slugify()`):

```php
<?php

$slugger = SluggerFactory::create('de');
echo $slugger->slugify('Über die Brücke');
echo $slugger->slugify('Straße');
```

German (`de`): ü → ue, ö → oe, ä → ae, ß → ss.

```php
<?php

$slugger = SluggerFactory::create('tr');
echo $slugger->slugify('İstanbul');
```

Turkish (`tr`): ı → i, İ → I, ş → s, ç → c, ğ → g.

Supported today: `de`, `tr`.

## Overrides

`mappings` on `slugify()` win over the locale for the same character:

```php
<?php

$slugger = SluggerFactory::create('de');
echo $slugger->slugify('Ü-Boot', mappings: ['Ü' => 'U']);
```

## Next

- [Home](index.md)
- [Usage](Usage.md)
- [Installation](Installation.md)
