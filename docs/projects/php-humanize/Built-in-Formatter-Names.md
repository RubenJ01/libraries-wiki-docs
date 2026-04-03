Use these keys when overriding built-in formatters via `HumanizerFactory::create(formatters: [...])` or when calling `apply()`.

## Built-in keys

- `fileSize`
- `dataRate`
- `ordinal`
- `abbreviate`
- `diffForHumans`
- `joinList`
- `pluralize`
- `toWords`
- `duration`
- `truncate`
- `readableDate`
- `number`
- `percentage`

## Example: override one built-in

```php
<?php

use Rjds\PhpHumanize\Formatter\FormatterInterface;
use Rjds\PhpHumanize\HumanizerFactory;

class MyNumberFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        return 'n/a';
    }

    public function getName(): string
    {
        return 'number';
    }
}

$humanizer = HumanizerFactory::create(
    formatters: [
        'number' => new MyNumberFormatter(),
    ]
);

echo $humanizer->number(1234.56); // "n/a"
```

## Notes

- Keys are case-sensitive.
- A formatter key must be a non-empty string.
- Formatter values must implement `FormatterInterface`.

