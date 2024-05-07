# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...errors.bad_request_error import BadRequestError
from ...errors.too_many_requests_error import TooManyRequestsError
from ...errors.unauthorized_error import UnauthorizedError
from ...types.api_error_response import ApiErrorResponse
from ...types.transaction_event import TransactionEvent
from ...types.transaction_event_monitoring_result import TransactionEventMonitoringResult

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TransactionEventsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(self, *, request: TransactionEvent) -> TransactionEventMonitoringResult:
        """
        ## POST Transaction Events

        `/events/transaction` endpoint allows you to operate on the [Transaction Events entity.](/guides/overview/entities#transaction-event)

        Transaction events are created after the initial `POST /transactions` call (which creates a transaction) and are used to:

        - Update the STATE of the transaction, using the `transactionState` field and manage the [Transaction Lifecycle](/guides/overview/entities#transaction-lifecycle-through-transaction-events)
        - Update the transaction details, using the `updatedTransactionAttributes` field.

        > If you have neither of the above two use cases, you do not need to use transaction events.

        ### Payload

        Each transaction event needs three mandatory fields:

        - `transactionState` - STATE of the transaction -> value is set to `CREATED` after `POST /transactions` call
        - `timestamp`- the timestamp of when the event was created or occured in your system
        - `transactionId` - The ID of the transaction for which this event is generated.

        In order to make individual events retrievable, you also need to pass in a unique `eventId` to the request body.

        Parameters:
            - request: TransactionEvent.
        ---
        from flagright import DeviceData, TransactionEvent, TransactionState
        from flagright.client import Flagright

        client = Flagright(
            api_key="YOUR_API_KEY",
        )
        client.transaction_events.create(
            request=TransactionEvent(
                transaction_state=TransactionState.SUCCESSFUL,
                timestamp=1431231244001.0,
                transaction_id="443dea26147a406b957d9ee3a1247b11",
                event_id="aaeeb166147a406b957dd9147a406b957",
                event_description="Transaction created",
                meta_data=DeviceData(
                    battery_level=76.3,
                    device_latitude=13.009711,
                    device_longitude=76.102898,
                    ip_address="79.144.2.20",
                    vpn_used=True,
                ),
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "events/transaction"),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(TransactionEventMonitoringResult, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 401:
            raise UnauthorizedError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 429:
            raise TooManyRequestsError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(self, event_id: str) -> TransactionEvent:
        """
        ### GET Transaction Events

        `/events/transaction` endpoint allows you to operate on the [Transaction Events entity.](/guides/overview/entities#transaction-event).

        You can retrieve any transaction event you created using the [POST Transaction Events](/api-reference/api-reference/transaction-events/create) call.

        Parameters:
            - event_id: str. Unique Transaction Identifier
        ---
        from flagright.client import Flagright

        client = Flagright(
            api_key="YOUR_API_KEY",
        )
        client.transaction_events.get(
            event_id="eventId",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"events/transaction/{event_id}"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(TransactionEvent, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 401:
            raise UnauthorizedError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 429:
            raise TooManyRequestsError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncTransactionEventsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(self, *, request: TransactionEvent) -> TransactionEventMonitoringResult:
        """
        ## POST Transaction Events

        `/events/transaction` endpoint allows you to operate on the [Transaction Events entity.](/guides/overview/entities#transaction-event)

        Transaction events are created after the initial `POST /transactions` call (which creates a transaction) and are used to:

        - Update the STATE of the transaction, using the `transactionState` field and manage the [Transaction Lifecycle](/guides/overview/entities#transaction-lifecycle-through-transaction-events)
        - Update the transaction details, using the `updatedTransactionAttributes` field.

        > If you have neither of the above two use cases, you do not need to use transaction events.

        ### Payload

        Each transaction event needs three mandatory fields:

        - `transactionState` - STATE of the transaction -> value is set to `CREATED` after `POST /transactions` call
        - `timestamp`- the timestamp of when the event was created or occured in your system
        - `transactionId` - The ID of the transaction for which this event is generated.

        In order to make individual events retrievable, you also need to pass in a unique `eventId` to the request body.

        Parameters:
            - request: TransactionEvent.
        ---
        from flagright import DeviceData, TransactionEvent, TransactionState
        from flagright.client import AsyncFlagright

        client = AsyncFlagright(
            api_key="YOUR_API_KEY",
        )
        await client.transaction_events.create(
            request=TransactionEvent(
                transaction_state=TransactionState.SUCCESSFUL,
                timestamp=1431231244001.0,
                transaction_id="443dea26147a406b957d9ee3a1247b11",
                event_id="aaeeb166147a406b957dd9147a406b957",
                event_description="Transaction created",
                meta_data=DeviceData(
                    battery_level=76.3,
                    device_latitude=13.009711,
                    device_longitude=76.102898,
                    ip_address="79.144.2.20",
                    vpn_used=True,
                ),
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "events/transaction"),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(TransactionEventMonitoringResult, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 401:
            raise UnauthorizedError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 429:
            raise TooManyRequestsError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(self, event_id: str) -> TransactionEvent:
        """
        ### GET Transaction Events

        `/events/transaction` endpoint allows you to operate on the [Transaction Events entity.](/guides/overview/entities#transaction-event).

        You can retrieve any transaction event you created using the [POST Transaction Events](/api-reference/api-reference/transaction-events/create) call.

        Parameters:
            - event_id: str. Unique Transaction Identifier
        ---
        from flagright.client import AsyncFlagright

        client = AsyncFlagright(
            api_key="YOUR_API_KEY",
        )
        await client.transaction_events.get(
            event_id="eventId",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"events/transaction/{event_id}"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(TransactionEvent, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 401:
            raise UnauthorizedError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 429:
            raise TooManyRequestsError(pydantic.parse_obj_as(ApiErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
