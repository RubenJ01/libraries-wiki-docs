Add the repository to your `composer.json` if needed:

```json
{
    "repositories": [
        {"type": "composer", "url": "https://ruben-jakob-digital-solutions.repo.repman.rubenjakob.com"}
    ]
}
```

Install the package:

```bash
composer require rjds/php-humanize
```

Basic setup:

```php
<?php

use Rjds\PhpHumanize\Humanizer;

$humanizer = new Humanizer();
```

## Next

- [Home](index.md)
- [Numbers](Numbers.md)
- [File Size](File-Size.md)
- [Duration](Duration.md)

