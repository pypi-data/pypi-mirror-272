import dataclasses
from logging import getLogger
from typing import Callable
from uuid import uuid4
from reactivex import Observable, compose, operators
from bittrade_binance_websocket.events.request_response import wait_for_response
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket

from bittrade_binance_websocket.models.response_message import ResponseMessage

logger = getLogger(__name__)


@dataclasses.dataclass
class EventRequest:
    method: str
    id: str
    params: dict

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        # if self.params.get("omitZeroBalances"):
        #     as_dict["params"]["omitZeroBalances"] = "true"
        return as_dict


def account_status(
    messages: Observable[ResponseMessage],
) -> Callable[[Observable[EnhancedWebsocket]], Observable[ResponseMessage]]:
    def socket_to_event_messages(
        socket: EnhancedWebsocket,
    ) -> Observable[ResponseMessage]:
        request_id = str(uuid4())
        params = {"omitZeroBalances": True}
        req = EventRequest(method="account.status", id=request_id, params=params)

        logger.info(f"account_status request, {req.to_dict()}")

        socket.send_message(req.to_dict())
        return messages.pipe(
            wait_for_response(request_id, 5.0),
            operators.do_action(lambda x: logger.info(x)),
        )

    return compose(operators.flat_map(socket_to_event_messages))
