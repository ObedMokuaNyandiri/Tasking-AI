from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from typing import Dict, List
from common.services.tool.action import *
from app.schemas.tool.action import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse, BaseListRequest
from common.models import Action, SerializePurpose

router = APIRouter()


@router.get(
    "/actions",
    tags=["Tool"],
    summary="List Actions",
    operation_id="list_actions",
    response_model=BaseSuccessListResponse,
)
async def api_list_actions(
    request: Request,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    actions, total, has_more = await list_actions(
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
    )
    return BaseSuccessListResponse(
        data=[action.to_dict(purpose=SerializePurpose.RESPONSE) for action in actions],
        fetched_count=len(actions),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/actions/{action_id}",
    tags=["Tool"],
    summary="Get Action",
    operation_id="get_action",
    response_model=BaseSuccessDataResponse,
)
async def api_get_action(
    action_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    action: Action = await get_action(
        action_id=action_id,
    )
    return BaseSuccessDataResponse(data=action.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/actions/bulk_create",
    tags=["Tool"],
    summary="Bulk Create Action",
    operation_id="bulk_create_action",
    response_model=BaseSuccessDataResponse,
)
async def api_bulk_create_actions(
    request: Request,
    data: ActionBulkCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    actions: List[Action] = await bulk_create_actions(
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    results = [action.to_dict(purpose=SerializePurpose.RESPONSE) for action in actions]
    return BaseSuccessDataResponse(data=results)


@router.post(
    "/actions/{action_id}",
    tags=["Tool"],
    summary="Update Action",
    operation_id="update_action",
    response_model=BaseSuccessDataResponse,
)
async def api_update_action(
    action_id: str,
    request: Request,
    data: ActionUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    action: Action = await update_action(
        action_id=action_id,
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    return BaseSuccessDataResponse(data=action.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/actions/{action_id}",
    tags=["Tool"],
    summary="Delete Action",
    operation_id="delete_action",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_action(
    action_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_action(
        action_id=action_id,
    )
    return BaseSuccessEmptyResponse()


@router.post(
    "/actions/{action_id}/run",
    tags=["Tool"],
    summary="Run Action",
    operation_id="run_action",
    response_model=BaseSuccessDataResponse,
)
async def api_run_action(
    action_id: str,
    request: Request,
    data: ActionRunRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    response: Dict = await run_action(
        action_id=action_id,
        parameters=data.parameters,
        headers=data.headers,
    )
    return BaseSuccessDataResponse(data=response)
