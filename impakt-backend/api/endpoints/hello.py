from flask import Blueprint, request
from flask_pydantic import validate
import json
from pydantic import BaseModel
import os

hello_blueprint = Blueprint("hello", __name__)


class HelloResponse(BaseModel):
    name: str


@hello_blueprint.route("/", methods=["GET"])
@validate(query=HelloResponse)
def get_hello():
    name = request.query_params.name
    return f"Hello, {name}!, {os.environ['PYTHON_ENV']}"
