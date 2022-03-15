from typing import Dict, List, Optional, Tuple, Union

import requests

from ..auth import Session
from ..common import *
from ..exceptions import *
from ..items.api import _transform_item_result
from ..items.models import *
from .models import *

__all__ = [
    "get_orders",
    "get_current_orders",
    "get_orders_by_username",
]


def get_orders(
    url_name: str,
    platform: Optional[Platform] = Platform.pc,
    include: Optional[IncludeOption] = None,
) -> Union[List[OrderRow], Tuple[List[OrderRow], ItemFull, List[ItemFull]]]:
    """Get orders of an item

    Args:
        url_name (str): unique name for an item
        platform (Optional[Platform], optional): platform. Defaults to Platform.pc.
        include (Optional[IncludeOption], optional):
            additional info.
            If ``IncludeOption.item`` is set, the info of the item will be returned additionally.
            Defaults to None.

    Returns:
        Union[List[OrderRow], Tuple[List[OrderRow], ItemFull, List[ItemFull]]]:
            The first is the order list.
            If ``IncludeOption.item`` is set, the same result of get_item method will be returned
            as the 2nd and 3rd return value.
    """
    res = requests.get(
        API_BASE_URL + f"/items/{url_name}/orders",
        params={"include": include},
        headers={"Platform": platform},
    )
    check_wm_response(res)
    json_obj = res.json()
    orders = list(map(lambda x: OrderRow.from_dict(x), json_obj["payload"]["orders"]))
    if include == IncludeOption.item:
        target_item, items_in_set = _transform_item_result(json_obj["include"]["item"])
        return orders, target_item, items_in_set
    else:
        return orders


def get_current_orders(sess: Session) -> Tuple[List[OrderItem], List[OrderItem]]:
    """See ``get_orders_by_username``

    Args:
        sess: session

    Returns:
        Tuple[List[OrderItem], List[OrderItem]]:
            the first is the list of the buy orders, the second is the list of sell orders
    """
    if sess.user.ingame_name is None or sess.user.ingame_name.strip() == "":
        raise RuntimeError("`ingame_name` of session is invalid.", sess)
    return get_orders_by_username(sess.user.ingame_name, sess)


def get_orders_by_username(
    username: str, sess: Optional[Session] = None
) -> Tuple[List[OrderItem], List[OrderItem]]:
    """Get orders of user

    Args:
        username (str): username
        sess (Session): session. If None, then set in guest mode. Defaults to None.

    Returns:
        Tuple[List[OrderItem], List[OrderItem]]:
            the first is the list of the buy orders, the second is the list of sell orders
    """
    if sess is not None:
        res = requests.get(
            API_BASE_URL + f"/profile/{username}/orders",
            **sess.to_header_dict(),
        )
    else:
        res = requests.get(
            API_BASE_URL + f"/profile/{username}/orders",
        )
    check_wm_response(res)
    json_obj = res.json()
    return (
        list(map(lambda x: OrderItem.from_dict(x), json_obj["payload"]["buy_orders"])),
        list(map(lambda x: OrderItem.from_dict(x), json_obj["payload"]["sell_orders"])),
    )
