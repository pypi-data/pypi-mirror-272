from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_delete_result import ChatDeleteResult
from ...types import Response


def _get_kwargs(
    chat_uuid: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/chats/{chat_uuid}/delete/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ChatDeleteResult]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChatDeleteResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChatDeleteResult]:
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
) -> Response[ChatDeleteResult]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatDeleteResult]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ChatDeleteResult]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatDeleteResult
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChatDeleteResult]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatDeleteResult]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ChatDeleteResult]:
    """Simple Viewset for modifying user profiles

    Args:
        chat_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatDeleteResult
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
        )
    ).parsed
