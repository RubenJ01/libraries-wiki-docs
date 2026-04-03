Use `pluralize()` to format quantities with correct singular/plural forms.

```php
<?php

// 1 item
echo $humanizer->pluralize(1, 'item');

// 5 items
echo $humanizer->pluralize(5, 'item');

// 3 children
echo $humanizer->pluralize(3, 'child', 'children');
```

