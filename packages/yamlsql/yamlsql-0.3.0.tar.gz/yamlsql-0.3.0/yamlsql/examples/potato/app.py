from sqlalchemy import StaticPool, create_engine

from yamlsql.core.server import YamlSQLServer
from yamlsql.examples.potato.potato import potato_crud

engine = create_engine(
    "sqlite:///:memory:",
    # "sqlite:///./app.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

server = YamlSQLServer(models=[potato_crud], engine=engine)
server.create_tables()

app = server.app
