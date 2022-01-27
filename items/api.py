import requests
from typing import Dict, List, Optional, Tuple, Union

from common import *
from .models import *


def list_items(lang: Optional[Language] = Language.en) -> List[ItemShort]:
    res = requests.get(
        API_BASE_URL + "/items",
        headers={"Language": lang.value if lang is not None else None},
    )
    res.raise_for_status()
    return list(map(lambda x: ItemShort.from_dict(x), res.json()["payload"]["items"]))


def get_item(
    url_name: str, platform: Optional[Platform] = Platform.pc
) -> Tuple[ItemFull, List[ItemFull]]:
    res = requests.get(
        API_BASE_URL + f"/items/{url_name}",
        headers={"Platform": platform.value if platform is not None else None},
    )
    res.raise_for_status()
    item_json = res.json()["payload"]["item"]
    return _transform_item_result(item_json)


def get_orders(
    url_name: str,
    platform: Optional[Platform] = Platform.pc,
    include: Optional[IncludeOption] = None,
) -> Union[List[OrderRow], Tuple[List[OrderRow], ItemFull, List[ItemFull]]]:
    res = requests.get(
        API_BASE_URL + f"/items/{url_name}/orders",
        params={"include": include.value if include is not None else None},
        headers={"Platform": platform.value if platform is not None else None},
    )
    json_obj = res.json()
    orders = list(map(lambda x: OrderRow.from_dict(x), json_obj["payload"]["orders"]))
    if include == IncludeOption.item:
        target_item, items_in_set = _transform_item_result(json_obj["include"]["item"])
        return orders, target_item, items_in_set
    else:
        return orders


def _transform_item_result(item_json) -> Tuple[ItemFull, List[ItemFull]]:
    # transform `zh-han*` to `zh_han*`
    for d in item_json["items_in_set"]:
        d: Dict
        for k in list(d.keys()):
            k: str
            if "-" in k:
                d[k.replace("-", "_")] = d[k]

    id = item_json["id"]
    items_in_set = list(map(lambda x: ItemFull.from_dict(x), item_json["items_in_set"]))

    target_item = None
    for item in items_in_set:
        if item.id == id:
            target_item = item
            break
    if target_item is None:
        raise RuntimeError("could not find item")
    return target_item, items_in_set
