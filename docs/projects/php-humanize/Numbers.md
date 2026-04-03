## Number Formatting

Use `number()` to format values with locale-aware separators.

```php
<?php

use Rjds\PhpHumanize\Humanizer;

$humanizer = new Humanizer();

// 1,234,567.89
echo $humanizer->number(1234567.89, 2);

// 1.234.567,89
echo $humanizer->number(1234567.89, 2, Humanizer::LOCALE_NL);
```

## Percentage Formatting

Use `percentage()` to render fractions or direct percentage values with locale-aware separators.

```php
<?php

// 15.3%
echo $humanizer->percentage(0.153, 1);

// 15,3%
echo $humanizer->percentage(0.153, 1, Humanizer::LOCALE_NL);

// 15.3%
echo $humanizer->percentage(15.3, 1, Humanizer::LOCALE_EN, false);
```

## Number Abbreviation

Use `abbreviate()` to shorten large numbers.

```php
<?php

// 1.5K
echo $humanizer->abbreviate(1500);

// 2.3M
echo $humanizer->abbreviate(2300000);

// 1B
echo $humanizer->abbreviate(1000000000);
```

## Number to Words

Use `toWords()` to write numbers in words.

```php
<?php

// forty-two
echo $humanizer->toWords(42);

// one thousand
echo $humanizer->toWords(1000);

// one million, two hundred thirty-four thousand, five hundred sixty-seven
echo $humanizer->toWords(1234567);
```

## See also

- [Ordinals](Ordinals.md)
- [File Size](File-Size.md)
- [Data Rate](Data-Rate.md)
