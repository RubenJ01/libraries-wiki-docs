`Rjds\PhpDto\DtoMapper` maps an associative array to a DTO class using the target class’s constructor.

## `map()`

```php
<?php

$mapper = new DtoMapper();
$instance = $mapper->map($data, TargetDto::class);
```

- **Constructor required**: the DTO class must define a constructor; otherwise mapping throws `Rjds\PhpDto\Exception\MappingException` (also usable as `InvalidArgumentException` because it extends it).
- **Parameter order**: constructor parameters are filled in declaration order.
- **Keys**: by default each parameter is read from a top-level key matching the parameter name. Use [MapFrom](MapFrom.md) to change the path.
- **Missing keys**: if a key is absent and the parameter has a default value, that default is used.
- **Casts and collections**: [CastTo](CastTo.md) and [ArrayOf](ArrayOf.md) run after the raw value is resolved from the input array.

## Errors

Failures throw `MappingException` with structured context for debugging large payloads:

- `getDtoClass()` — DTO class where the failure applies (innermost nested DTO when an `#[ArrayOf]` element fails).
- `getParameterName()` / `getMapKey()` — constructor parameter and resolved source key (including dot notation from `#[MapFrom]`); on wrapped nested failures these refer to the **parent** list parameter.
- `getArrayIndex()` — index in an `#[ArrayOf]` list when relevant.
- `getParentDtoClass()` — set when a nested `#[ArrayOf]` mapping wraps an inner failure.
- `getPrevious()` / `getPreviousMappingException()` — inner `MappingException` when nested mapping failed.

Unsupported `#[CastTo]` types, missing constructors, non-array `#[ArrayOf]` items, and nested mapping errors are reported with these fields where applicable.

## PHPStan

The package ships `phpstan-extension.neon` (see the repository root). Include it in your PHPStan config so `DtoMapper::map()` is narrowed to the concrete DTO when the second argument is a class literal (`ArtistDto::class`) or a `class-string<SpecificDto>` type. The main repository README describes the same setup.

## Next

- [Home](index.md)
- [MapFrom](MapFrom.md)
