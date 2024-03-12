import os
from dotenv import dotenv_values


def load_dynamic_env() -> None:
    # check if the environment is development or production
    # and load the appropriate .env file
    # PYTHON_ENV is set in the Dockerfile
    if os.getenv("PYTHON_ENV") == "development":
        config = {
            **dotenv_values(".env.development"),
            **dotenv_values(".env.local"),
            **os.environ,
        }
    elif os.getenv("PYTHON_ENV") == "production":
        config = {
            **dotenv_values(".env.production"),
            **dotenv_values(".env.local"),
            **os.environ,
        }
    else:
        raise ValueError("Invalid value for PYTHON_ENV")

    os.environ.update(config)
