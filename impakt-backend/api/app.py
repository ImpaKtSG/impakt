from endpoints import hello_blueprint
from utils import AppException, load_dynamic_env
from flask import Flask
import os
import sys

# since this is the entrypoint for the application
# we need to add the current working directory to the path
# so that we can import everything from the project
sys.path.append(os.getcwd())

# load the environment variables
load_dynamic_env()


app = Flask(__name__)


@app.errorhandler(AppException)
def handle_error(error: AppException):
    response = error.to_dict()

    app.logger.error(f"{response.get('type')}: {response.get('message')}")
    return response, error.status_code


if __name__ == "__main__":
    app.register_blueprint(hello_blueprint, url_prefix="/hello")
    app.run(host="0.0.0.0", port=8080, debug=os.getenv("PYTHON_ENV", False))
