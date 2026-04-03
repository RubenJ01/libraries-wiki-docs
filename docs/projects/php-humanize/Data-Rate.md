Use `dataRate()` to convert bytes per second into human-readable transfer rates.

```php
<?php

// 1.5 KB/s
echo $humanizer->dataRate(1536);

// 1 MB/s
echo $humanizer->dataRate(1048576);

// 1 GB/s
echo $humanizer->dataRate(1073741824);

// Custom precision: 1.5625 KB/s
echo $humanizer->dataRate(1600, 4);
```

