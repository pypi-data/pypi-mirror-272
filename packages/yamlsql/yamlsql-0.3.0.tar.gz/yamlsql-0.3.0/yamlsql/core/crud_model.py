from dataclasses import dataclass
from typing import Any, Callable, Optional, Type

from pydantic import BaseModel

from yamlsql.utils.text import snake_case


@dataclass(frozen=True)
class CRUDModel:
    name: str
    create_db_model: Callable[[Any], Any]
    schema: Type[BaseModel]
    create_schema: Optional[Type[BaseModel]] = None
    update_schema: Optional[Type[BaseModel]] = None

    @property
    def schema_name(self):
        return snake_case(self.name)

    @property
    def json_schema(self):
        return self.schema.schema()
