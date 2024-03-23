from quart import Blueprint, Request
from quart_schema import validate_response, validate_request
from pydantic import BaseModel
import os
from models.tables import Company

hello_blueprint = Blueprint("hello", __name__)


class HelloResponse(BaseModel):
    name: str


@hello_blueprint.route("/", methods=["GET"])
async def get_hello():
    ret = await Company.test()
    return str(ret)
