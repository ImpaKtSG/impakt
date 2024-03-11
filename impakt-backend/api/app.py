from endpoints import hello_blueprint
from utils import AppException
from flask import Flask
from dotenv import dotenv_values
import os

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

app = Flask(__name__)


@app.errorhandler(AppException)
def handle_error(error: AppException):
    response = error.to_dict()

    app.logger.error(f"{response.get('type')}: {response.get('message')}")
    return response, error.status_code


if __name__ == "__main__":
    app.register_blueprint(hello_blueprint, url_prefix="/hello")
    app.run(host="0.0.0.0", port=8080, debug=os.getenv("PYTHON_ENV", False))
