Use `fileSize()` to convert bytes to human-readable units.

```php
<?php

// 1.5 KB
echo $humanizer->fileSize(1536);

// 5.2 MB
echo $humanizer->fileSize(5452595);

// 2 GB
echo $humanizer->fileSize(2147483648);

// Custom precision: 1.5 KB
echo $humanizer->fileSize(1536, 2);
```

## See also

- [Data Rate](Data-Rate.md)
- [Numbers](Numbers.md)

