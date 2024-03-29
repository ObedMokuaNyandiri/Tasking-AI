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


async def list_actions(params: Dict = None):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions"
        response = await session.get(request_url, params=params)
        return ResponseWrapper(response.status, await response.json())


async def get_action(action_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions/{action_id}"
        response = await session.get(request_url)
        return ResponseWrapper(response.status, await response.json())


async def create_action(payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions/bulk_create"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def update_action(action_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions/{action_id}"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def delete_action(action_id: str):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions/{action_id}"
        response = await session.delete(request_url)
        return ResponseWrapper(response.status, await response.json())


async def run_action(action_id: str, payload: Dict):
    headers = get_headers(Token)
    async with aiohttp.ClientSession(headers=headers) as session:
        request_url = f"{BASE_URL}/actions/{action_id}/run"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())
