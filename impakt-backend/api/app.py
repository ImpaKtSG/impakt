#!/usr/bin/env python
from endpoints import hello_blueprint
from utils import AppException, AppExceptions, load_dynamic_env
from quart_schema import RequestSchemaValidationError
from quart import Quart
from quart_cors import cors
from quart_schema import QuartSchema
import os
import sys

# since this is the entrypoint for the application
# we need to add the current working directory to the path
# so that we can import everything from the project
sys.path.append(os.getcwd())

# load the environment variables
load_dynamic_env()

app = Quart(__name__)
app = cors(app, allow_origin=os.getenv("API_URL", None))

# allow validation of request schemas
QuartSchema(app)


@app.errorhandler(AppException)
def handle_error(error: AppException):
    response = error.to_dict()

    app.logger.error(f"{response.get('type')}: {response.get('message')}")
    return response, error.status_code


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error: RequestSchemaValidationError):

    # create an app exception to raise
    response = AppExceptions.VALIDATION_ERROR(error).to_dict()
    return response, response.get("status_code")


if __name__ == "__main__":
    app.register_blueprint(hello_blueprint, url_prefix="/hello")
    app.run(host="0.0.0.0", port=8080, debug=os.getenv("PYTHON_ENV", False))
