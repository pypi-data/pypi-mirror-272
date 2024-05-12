from pydantic import BaseModel
from sqlalchemy import Column, Float, String

from yamlsql.core.crud_model import CRUDModel


class DraftPotato(BaseModel):
    uid: str
    thickness: float
    mass: float
    color: str
    type: str


class Potato(DraftPotato):
    class Config:
        orm_mode = True


def create_sqlalchemy_model(Base):
    class PotatoModel(Base):
        __tablename__ = "potatoes"
        uid = Column(String, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String)
        type = Column(String)

    return PotatoModel


potato_crud = CRUDModel(
    name="Potato",
    schema=Potato,
    create_schema=DraftPotato,
    create_db_model=create_sqlalchemy_model,
)
