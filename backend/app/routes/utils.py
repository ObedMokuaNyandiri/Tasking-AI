from common.error import raise_http_error, ErrorCode
from starlette.requests import Request
from fastapi import HTTPException
from config import CONFIG
from typing import Dict
from common.services.auth.admin import verify_admin_token
from common.services.auth.apikey import verify_apikey


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))


async def app_admin_auth_info_required(request: Request) -> Dict:
    ret = {}

    # 1. extract token
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        ret["token"] = authorization[7:]

    if not ret.get("token"):
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Token is missing")

    # 2. verify token
    admin = await verify_admin_token(token=ret["token"])
    ret["admin_id"] = admin.admin_id

    return ret


async def api_auth_info_required(request: Request) -> Dict:
    apikey = None

    # 1. extract apikey
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        apikey = authorization[7:]

    if not apikey:
        raise_http_error(ErrorCode.APIKEY_VALIDATION_FAILED, message="API Key validation failed")

    # 2. verify apikey
    await verify_apikey(apikey=apikey)
    ret = {
        "apikey": apikey,
    }

    return ret


async def auth_info_required(request: Request) -> Dict:
    if CONFIG.WEB:
        return await app_admin_auth_info_required(request)

    elif CONFIG.API:
        return await api_auth_info_required(request)

    raise NotImplementedError("Unknown auth type")
