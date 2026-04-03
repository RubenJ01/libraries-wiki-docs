Use `joinList()` to convert arrays into natural-language lists.

```php
<?php

// Alice, Bob, and Charlie
echo $humanizer->joinList(['Alice', 'Bob', 'Charlie']);

// Alice and Bob
echo $humanizer->joinList(['Alice', 'Bob']);

// Alice or Bob
echo $humanizer->joinList(['Alice', 'Bob'], 'or');

// Alice; Bob; and Charlie
echo $humanizer->joinList(['Alice', 'Bob', 'Charlie'], 'and', '; ');
```

