import pydantic
from pydantic import BaseModel
from typing import (Any)

class HttpCode:
    _200=200
    _400=400
    _403=403
    _404=404
    _500=500

class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }