Use `diffForHumans()` to format date/time differences.

```php
<?php

use DateTimeImmutable;

$now = new DateTimeImmutable();

// 5 minutes ago
echo $humanizer->diffForHumans($now->modify('-5 minutes'), $now);

// 2 weeks ago
echo $humanizer->diffForHumans($now->modify('-14 days'), $now);

// in 2 hours
echo $humanizer->diffForHumans($now->modify('+2 hours'), $now);
```

