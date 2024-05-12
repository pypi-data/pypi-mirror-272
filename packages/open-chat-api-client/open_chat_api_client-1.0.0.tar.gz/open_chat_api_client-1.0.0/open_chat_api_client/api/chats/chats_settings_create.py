from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_settings import ChatSettings
from ...models.set_chat_title_request import SetChatTitleRequest
from ...types import Response


def _get_kwargs(
    chat_uuid: str,
    *,
    body: SetChatTitleRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/chats/{chat_uuid}/settings/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ChatSettings]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChatSettings.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ChatSettings]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SetChatTitleRequest,
) -> Response[ChatSettings]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):
        body (SetChatTitleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatSettings]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SetChatTitleRequest,
) -> Optional[ChatSettings]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):
        body (SetChatTitleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatSettings
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SetChatTitleRequest,
) -> Response[ChatSettings]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):
        body (SetChatTitleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatSettings]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SetChatTitleRequest,
) -> Optional[ChatSettings]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):
        body (SetChatTitleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatSettings
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            body=body,
        )
    ).parsed
