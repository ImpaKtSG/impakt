from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import Engine


# SQLAlchemy engine
def make_engine(
    *,
    loc: str = "localhost:5432",
    username: str = "postgres",
    password: str = "postgres",
    database: str = "impakt",
    echo: bool = False,
    debug: bool = False,
) -> Engine:

    url = f"postgresql+asyncpg://{username}:{password}@{loc}/{database}"
    engine = create_async_engine(
        url,
        echo=echo,
        echo_pool=debug,
        isolation_level="AUTOCOMMIT",
    )
    return engine
