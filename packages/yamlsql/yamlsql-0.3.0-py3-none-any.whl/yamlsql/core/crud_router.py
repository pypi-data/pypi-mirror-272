from fastapi_crudrouter import SQLAlchemyCRUDRouter

from yamlsql.core.crud_model import CRUDModel


def create_crud_router(model: CRUDModel, Base, get_db):
    return SQLAlchemyCRUDRouter(
        schema=model.schema,
        create_schema=model.create_schema,
        db_model=model.create_db_model(Base),
        db=get_db,
        prefix=f"entity/{model.schema_name}",
        tags=["crud"],
    )
