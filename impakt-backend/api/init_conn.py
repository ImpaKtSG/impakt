from db.client import make_engine
import os

# Create the engine
engine = make_engine(
    loc=f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    echo=False,
    debug=False,
)
