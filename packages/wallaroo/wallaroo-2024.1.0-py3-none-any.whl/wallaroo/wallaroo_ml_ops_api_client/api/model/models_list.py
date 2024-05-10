from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.models_list_body import ModelsListBody
from ...models.models_list_response_200 import ModelsListResponse200
from ...models.models_list_response_400 import ModelsListResponse400
from ...models.models_list_response_401 import ModelsListResponse401
from ...models.models_list_response_500 import ModelsListResponse500
from ...types import Response


def _get_kwargs(
    *,
    body: ModelsListBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/api/models/list",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ModelsListResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ModelsListResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ModelsListResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ModelsListResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelsListBody,
) -> Response[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        body (ModelsListBody):  Workspace model retrieval request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelsListBody,
) -> Optional[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        body (ModelsListBody):  Workspace model retrieval request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelsListBody,
) -> Response[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        body (ModelsListBody):  Workspace model retrieval request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelsListBody,
) -> Optional[
    Union[
        ModelsListResponse200,
        ModelsListResponse400,
        ModelsListResponse401,
        ModelsListResponse500,
    ]
]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        body (ModelsListBody):  Workspace model retrieval request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
