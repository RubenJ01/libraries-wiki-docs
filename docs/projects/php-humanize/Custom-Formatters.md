The library supports creating custom formatters without modifying the core library. This is useful for adding domain-specific formatting, building plugins, or extending functionality.

## Choose your registration style

- Use `register()` when you add formatters at runtime on an existing `Humanizer`.
- Use `HumanizerFactory::create()` when you want one pre-configured instance with defaults and formatter overrides.

## Quick Start

```php
<?php

use Rjds\PhpHumanize\Formatter\FormatterInterface;
use Rjds\PhpHumanize\Humanizer;

class RomanNumeralFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        $number = (int)($args[0] ?? 0);
        return $this->toRoman($number);
    }

    public function getName(): string
    {
        return 'roman';
    }

    private function toRoman(int $number): string { /* ... */ }
}

// Register and use
$humanizer = new Humanizer();
$humanizer->register('roman', new RomanNumeralFormatter());

echo $humanizer->roman(42);           // "XLII"
echo $humanizer->apply('roman', 100); // "C"
```

## Factory-based registration (recommended for app setup)

```php
<?php

use Rjds\PhpHumanize\Formatter\FormatterInterface;
use Rjds\PhpHumanize\HumanizerFactory;

class RomanNumeralFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        return 'XLII';
    }

    public function getName(): string
    {
        return 'roman';
    }
}

$humanizer = HumanizerFactory::create(
    formatters: [
        'roman' => new RomanNumeralFormatter(),
    ]
);

echo $humanizer->roman(42); // "XLII"
```

## Override a built-in formatter

You can replace built-ins by providing the same key used by the registry:

```php
<?php

use Rjds\PhpHumanize\Formatter\FormatterInterface;
use Rjds\PhpHumanize\HumanizerFactory;

class MyFileSizeFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        return 'custom-size';
    }

    public function getName(): string
    {
        return 'fileSize';
    }
}

$humanizer = HumanizerFactory::create(
    formatters: [
        'fileSize' => new MyFileSizeFormatter(), // overrides built-in fileSize
    ]
);
```

For all built-in keys, see [Built-in Formatter Names](Built-in-Formatter-Names.md).

## The FormatterInterface

All custom formatters must implement `FormatterInterface`:

```php
<?php

interface FormatterInterface
{
    public function format(...$args): string;
    public function getName(): string;
}
```

### Methods

**`format(...$args): string`**
- Core formatting logic
- Accepts any variadic arguments needed by your formatter
- Must return a string

**`getName(): string`**
- Returns the formatter's unique name
- Used for registration and invocation
- Should be lowercase, camelCase (e.g., 'roman', 'temperature')

## Usage Patterns

After registering a formatter, you can use it in multiple ways:

### 1. Magic Method (Recommended)
```php
<?php

$humanizer->register('roman', new RomanNumeralFormatter());
echo $humanizer->roman(42); // "XLII"
```

### 2. apply() Method
```php
<?php

echo $humanizer->apply('roman', 42); // "XLII"
```

### 3. Direct Registry
```php
<?php

$formatter = $humanizer->getRegistry()->get('roman');
echo $formatter->format(42); // "XLII"
```

## Examples

### Temperature Converter

```php
<?php

class TemperatureFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        $celsius = (float)($args[0] ?? 0);
        $fahrenheit = ($celsius * 9/5) + 32;
        return round($fahrenheit, 1) . '°F';
    }

    public function getName(): string
    {
        return 'temperature';
    }
}

$h = new Humanizer();
$h->register('temperature', new TemperatureFormatter());
echo $h->temperature(25); // "77°F"
```

### Percentage Formatter

```php
<?php

class PercentageFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        $value = (float)($args[0] ?? 0);
        $decimals = (int)($args[1] ?? 2);
        return number_format($value, $decimals) . '%';
    }

    public function getName(): string
    {
        return 'percentage';
    }
}

$h = new Humanizer();
$h->register('percentage', new PercentageFormatter());
echo $h->percentage(99.5);  // "99.50%"
echo $h->percentage(100, 0);// "100%"
```

### Boolean to Text

```php
<?php

class BooleanFormatter implements FormatterInterface
{
    public function format(...$args): string
    {
        $value = (bool)($args[0] ?? false);
        return $value ? 'Yes' : 'No';
    }

    public function getName(): string
    {
        return 'boolean';
    }
}

$h = new Humanizer();
$h->register('boolean', new BooleanFormatter());
echo $h->boolean(true);  // "Yes"
echo $h->boolean(false); // "No"
```

## Fluent Registration

Register multiple formatters at once:

```php
<?php

$humanizer = new Humanizer()
    ->register('roman', new RomanNumeralFormatter())
    ->register('temperature', new TemperatureFormatter())
    ->register('percentage', new PercentageFormatter());

echo $humanizer->roman(42);        // "XLII"
echo $humanizer->temperature(25);  // "77°F"
echo $humanizer->percentage(99.5); // "99.50%"
```

## Auto-Discovery

For plugin systems or bulk registration, automatically discover formatters from a directory:

```php
<?php

$humanizer = new Humanizer();
$humanizer->getRegistry()->autoDiscover(
    __DIR__ . '/Formatters',
    'MyApp\Formatters'
);
```

All classes in that directory implementing `FormatterInterface` will be automatically registered using their `getName()` value.

### Directory Structure
```
MyApp/
└── Formatters/
    ├── RomanNumeralFormatter.php  (getName() returns 'roman')
    ├── TemperatureFormatter.php   (getName() returns 'temperature')
    └── PercentageFormatter.php    (getName() returns 'percentage')
```

After auto-discovery:
```php
<?php

$humanizer->roman(42);
$humanizer->temperature(25);
$humanizer->percentage(99.5);
```

## Testing Your Formatter

```php
<?php
use PHPUnit\Framework\TestCase;
use MyApp\Formatters\RomanNumeralFormatter;

class RomanNumeralFormatterTest extends TestCase
{
    private RomanNumeralFormatter $formatter;

    protected function setUp(): void
    {
        $this->formatter = new RomanNumeralFormatter();
    }

    public function testFormatsNumbers(): void
    {
        $this->assertEquals('XLII', $this->formatter->format(42));
        $this->assertEquals('C', $this->formatter->format(100));
    }

    public function testReturnsName(): void
    {
        $this->assertEquals('roman', $this->formatter->getName());
    }
}
```

## Best Practices

1. **Use clear, descriptive names** - Make `getName()` self-explanatory
2. **Handle edge cases** - Validate and handle unusual inputs gracefully
3. **Keep it focused** - One formatter should do one thing well
4. **Add documentation** - Document expected arguments and output format
5. **Write tests** - Test your formatter independently
6. **Use type hints** - Cast arguments to expected types safely
7. **Fail gracefully** - Return sensible defaults for invalid input

## Common Issues

### "Formatter not registered"
Make sure you call `register()` before using the formatter:
```php
<?php

$humanizer->register('myFormatter', new MyFormatter()); // Required!
$humanizer->myFormatter($args); // Now it works
```

With `HumanizerFactory::create()`, make sure your `formatters` array uses:
- a non-empty string key (`'roman'`, `'fileSize'`, etc.)
- a value that implements `FormatterInterface`

### Magic method not working
The magic method name must match the registered name exactly:
```php
<?php

$humanizer->register('roman', new RomanNumeralFormatter());
$humanizer->roman(42);  // ✅ Works (matches registered name)
$humanizer->Roman(42);  // ❌ Fails (case-sensitive)
```

### Arguments not being passed
Use variadic arguments in `format()`:
```php
<?php

// ✅ Correct
public function format(...$args): string {
    $arg1 = $args[0] ?? null;
    $arg2 = $args[1] ?? null;
}

// ❌ Won't work with dynamic calls
public function format(string $arg1, string $arg2): string { }
```

## See Also

- [Time Difference](Time-Difference.md) — built-in `diffForHumans()`
- [File Size](File-Size.md) — built-in `fileSize()`
- [Numbers](Numbers.md) — built-in numeric formatters

