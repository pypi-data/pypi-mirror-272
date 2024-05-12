from typing import List

from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from yamlsql.core.crud_model import CRUDModel
from yamlsql.core.crud_router import create_crud_router
from yamlsql.core.schema_router import create_schema_router


class YamlSQLServer:
    def __init__(self, models: List[CRUDModel], engine, prefix="/api/v0"):
        self.models = models
        self.engine = engine

        self.app = FastAPI()
        self.app.router.prefix = prefix

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        self.Base = declarative_base()

        def get_db():
            session = SessionLocal()
            try:
                yield session
                session.commit()
            finally:
                session.close()

        self.app.include_router(create_schema_router(models))

        for m in models:
            self.app.include_router(create_crud_router(m, self.Base, get_db))

    def create_tables(self):
        self.Base.metadata.create_all(bind=self.engine)
