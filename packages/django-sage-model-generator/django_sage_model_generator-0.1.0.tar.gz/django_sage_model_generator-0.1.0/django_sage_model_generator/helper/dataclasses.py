from dataclasses import dataclass
from enum import StrEnum

class DBMLRelation(StrEnum):
    OneToOne = '-'
    ManyToOne = '>'
    OneToMany = '<'
    ManyToMany = '<>'
    @staticmethod
    def from_str(value: str) -> 'DBMLRelation':
        if value == '-':
            return DBMLRelation.OneToOne
        elif value == '>':
            return DBMLRelation.ManyToOne
        elif value == '<':
            return DBMLRelation.OneToMany
        elif value == '<>':
            return DBMLRelation.ManyToMany
        else:
            raise ValueError(f"Invalid DBMLRelation value: {value}")

@dataclass(frozen=True)
class TableRelation:
    name: str
    fk_field: str
    rel_type: DBMLRelation
    to_table: str
    to_field: str
