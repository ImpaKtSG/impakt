from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
import os
from utils import load_dynamic_env


# SQLAlchemy engine
def make_engine(
    *,
    loc: str = "localhost:5432",
    username: str = "postgres",
    password: str = "postgres",
    database: str = "impakt",
    echo: bool = False,
    debug: bool = False,
) -> AsyncEngine:

    url = f"postgresql+asyncpg://{username}:{password}@{loc}/{database}"
    engine = create_async_engine(
        url,
        echo=echo,
        echo_pool=debug,
        isolation_level="AUTOCOMMIT",
    )
    return engine


def make_session(engine: AsyncEngine) -> AsyncSession:
    Session = async_sessionmaker(engine, expire_on_commit=False)
    return Session()

load_dynamic_env()

# Create the engine
engine = make_engine(
    loc=f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    echo=False,
    debug=False,
)
