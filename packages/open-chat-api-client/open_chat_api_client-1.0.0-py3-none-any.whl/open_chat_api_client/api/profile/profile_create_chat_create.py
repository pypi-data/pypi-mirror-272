from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_creation_response import ChatCreationResponse
from ...models.send_message import SendMessage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_uuid: str,
    *,
    body: SendMessage,
    contact_secret: Union[Unset, str] = UNSET,
    reveal_secret: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["contact_secret"] = contact_secret

    params["reveal_secret"] = reveal_secret

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/profile/{user_uuid}/create_chat",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ChatCreationResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChatCreationResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChatCreationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SendMessage,
    contact_secret: Union[Unset, str] = UNSET,
    reveal_secret: Union[Unset, str] = UNSET,
) -> Response[ChatCreationResponse]:
    """
    Args:
        user_uuid (str):
        contact_secret (Union[Unset, str]):
        reveal_secret (Union[Unset, str]):
        body (SendMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatCreationResponse]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
        body=body,
        contact_secret=contact_secret,
        reveal_secret=reveal_secret,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SendMessage,
    contact_secret: Union[Unset, str] = UNSET,
    reveal_secret: Union[Unset, str] = UNSET,
) -> Optional[ChatCreationResponse]:
    """
    Args:
        user_uuid (str):
        contact_secret (Union[Unset, str]):
        reveal_secret (Union[Unset, str]):
        body (SendMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatCreationResponse
    """

    return sync_detailed(
        user_uuid=user_uuid,
        client=client,
        body=body,
        contact_secret=contact_secret,
        reveal_secret=reveal_secret,
    ).parsed


async def asyncio_detailed(
    user_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SendMessage,
    contact_secret: Union[Unset, str] = UNSET,
    reveal_secret: Union[Unset, str] = UNSET,
) -> Response[ChatCreationResponse]:
    """
    Args:
        user_uuid (str):
        contact_secret (Union[Unset, str]):
        reveal_secret (Union[Unset, str]):
        body (SendMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatCreationResponse]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
        body=body,
        contact_secret=contact_secret,
        reveal_secret=reveal_secret,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_uuid: str,
    *,
    client: AuthenticatedClient,
    body: SendMessage,
    contact_secret: Union[Unset, str] = UNSET,
    reveal_secret: Union[Unset, str] = UNSET,
) -> Optional[ChatCreationResponse]:
    """
    Args:
        user_uuid (str):
        contact_secret (Union[Unset, str]):
        reveal_secret (Union[Unset, str]):
        body (SendMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatCreationResponse
    """

    return (
        await asyncio_detailed(
            user_uuid=user_uuid,
            client=client,
            body=body,
            contact_secret=contact_secret,
            reveal_secret=reveal_secret,
        )
    ).parsed
