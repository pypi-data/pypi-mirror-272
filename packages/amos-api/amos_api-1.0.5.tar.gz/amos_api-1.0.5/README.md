# amos api

主要用于定义离线分析中的 API 规范以及通用的 Response 等

## 快速开始

```py
from fastapi import (FastAPI, Body)
from amos_api import (BaseResponse, HttpCode)
from starlette.responses import RedirectResponse

async def document():
    # return RedirectResponse(url="/docs")
    return RedirectResponse(url="/redoc")

def mount_app_routes(app: FastAPI):
    app.get("/",
            response_model=BaseResponse,
            summary="swagger 文档")(document)
    # tag items
    app.post("/user",
             tags=["User"],
             summary="用户信息",
             )(userInfo)

async def userInfo(name: str=Body(..., description="用户名称", examples=["ray"])) -> BaseResponse:
    return BaseResponse(data={"seq":"1", "name": name,})

async def userList(name: str=Body(..., description="用户名称", examples=["ray"])) -> BaseResponse:
    try:
        dblist()
    except Exception as e:
        msg = f"未知错误{e}"
        return BaseResponse(code=HttpCode._500, msg=msg)
    return BaseResponse(data=[])
```

- `HttpCode._200` 请求成功,正常 code 值，BaseResponse 如果不设置code时，默认值。
- `HttpCode._400` 错误的请求，比如参数错误
- `HttpCode._403` 禁止访问的资源
- `HttpCode._404` 未找到
- `HttpCode._422` 常用于参数错误
- `HttpCode._500` 服务器错误，内部错误
- `HttpCode._522` 服务器错误，内部错误
  