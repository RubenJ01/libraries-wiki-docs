Use `duration()` to format seconds as a human-readable duration.

```php
<?php

// 1 minute, 30 seconds
echo $humanizer->duration(90);

// 1 hour, 1 minute, 1 second
echo $humanizer->duration(3661);

// 1 day
echo $humanizer->duration(86400);

// Precision: 1 hour
echo $humanizer->duration(3661, 1);
```

