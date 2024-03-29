import aiohttp
from typing import Dict

from tests.common.utils import ResponseWrapper, get_headers, Token
from tests.settings import HOST
from config import CONFIG

if CONFIG.WEB:
    BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"
elif CONFIG.API:
    BASE_URL = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.API_ROUTE_PREFIX}"
    from tests.common.utils import APIKEY
    Token = APIKEY


async def chat_completion(params: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/inference/chat_completion"
        response = await session.post(request_url, json=params)
        return ResponseWrapper(response.status, await response.json())
