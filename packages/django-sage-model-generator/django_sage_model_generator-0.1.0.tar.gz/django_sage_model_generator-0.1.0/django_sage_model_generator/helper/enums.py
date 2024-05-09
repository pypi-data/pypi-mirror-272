from enum import Enum


class FieldType(Enum):
    INT = 'IntegerField'
    VARCHAR = 'CharField'
    DATETIME = 'DateTimeField'
    TIMESTAMP = 'DateTimeField'
    BOOLEAN = 'BooleanField'
    SLUG = 'SlugField'
    DECIMAL = 'DecimalField'
    FLOAT = 'FloatField'
    IMAGE = 'ImageField'
