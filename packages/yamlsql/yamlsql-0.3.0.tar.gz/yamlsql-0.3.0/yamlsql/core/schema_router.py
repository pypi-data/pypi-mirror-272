from typing import Dict, List

from fastapi import APIRouter

from yamlsql.core.crud_model import CRUDModel


def create_schema_router(models: List[CRUDModel]):
    router = APIRouter(tags=["schema"])

    schema_lookup = {m.schema_name: m.json_schema for m in models}
    schema_names = list(schema_lookup.keys())

    @router.get("/schemas", operation_id="get_schemas", response_model=List[str])
    def get_schemas():
        return schema_names

    @router.get("/schema/{name}", operation_id="get_schema", response_model=Dict)
    def get_schema(name: str):
        return schema_lookup[name].json_schema

    return router
