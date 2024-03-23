from quart import Blueprint, Request
from quart_schema import validate_response, validate_querystring, validate_request

from models.tables import Company
from dataclasses import dataclass


hello_blueprint = Blueprint("hello", __name__)


@dataclass
class HelloResponse:
    message: str
    a: int


@hello_blueprint.route("/", methods=["GET"])
@validate_querystring(HelloResponse)
async def get_hello(query_args: HelloResponse):
    ret = await Company.test()
    return str(ret)
