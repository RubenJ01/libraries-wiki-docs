Use `truncate()` to shorten long text without cutting a word in half.

```php
<?php

// The quick brown fox…
echo $humanizer->truncate('The quick brown fox jumps over the lazy dog', 20);

// Hello World (no truncation needed)
echo $humanizer->truncate('Hello World', 50);

// The quick brown...
echo $humanizer->truncate('The quick brown fox', 15, '...');
```

