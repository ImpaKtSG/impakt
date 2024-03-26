#!/usr/bin/env python
from endpoints import hello_blueprint
from utils import AppException, AppExceptions, load_dynamic_env
from quart_schema import RequestSchemaValidationError
from quart import Quart
from quart_cors import cors
from quart_schema import QuartSchema
import os
import sys
from datetime import datetime
import atexit

# since this is the entrypoint for the application
# we need to add the current working directory to the path
# so that we can import everything from the project
sys.path.append(os.getcwd())

# load the environment variables
load_dynamic_env()

# create the app
app = Quart(__name__)
app = cors(app, allow_origin=os.getenv("API_URL", None))

# allow validation of request schemas
QuartSchema(app)


# handle errors manually thrown by the application
@app.errorhandler(AppException)
def handle_error(error: AppException):
    response = error.to_dict()

    app.logger.error(f"{response.get('type')}: {response.get('message')}")
    return response, error.status_code


# handle errors thrown by the request schema validation
@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error: RequestSchemaValidationError):

    # create an app exception to raise
    response = AppExceptions.VALIDATION_ERROR(error).to_dict()
    return response, response.get("status_code")


# register the blueprints
# this is a map of routes to blueprints
to_register = {"/hello": hello_blueprint}

for route, blueprint in to_register.items():
    app.register_blueprint(blueprint, url_prefix=route)


# register on exit cleanup
def cleanup():
    app.logger.info(f"Shutting down at time: {datetime.now().isoformat()}")


atexit.register(cleanup)

# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=os.getenv("PYTHON_ENV", False))
