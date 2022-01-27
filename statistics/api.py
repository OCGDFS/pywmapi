import requests
from typing import Dict, List, Optional, Tuple

from common import *
from .models import *


def get_statistic(
    url_name: str, platform: Optional[Platform] = Platform.pc
) -> Statistic:
    res = requests.get(
        API_BASE_URL + f"/items/{url_name}/statistics",
        headers={"Platform": platform.value if platform is not None else None},
    )
    res.raise_for_status()
    payload = res.json()["payload"]
    return Statistic(
        closed_48h=list(
            map(
                lambda x: StatisticClosed.from_dict(x),
                payload["statistics_closed"]["48hours"],
            )
        ),
        closed_90d=list(
            map(
                lambda x: StatisticClosed.from_dict(x),
                payload["statistics_closed"]["90days"],
            )
        ),
        live_48h=list(
            map(
                lambda x: StatisticLive.from_dict(x),
                payload["statistics_live"]["48hours"],
            )
        ),
        live_90d=list(
            map(
                lambda x: StatisticLive.from_dict(x),
                payload["statistics_live"]["90days"],
            )
        ),
    )
