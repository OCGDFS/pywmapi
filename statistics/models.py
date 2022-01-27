from ctypes import cast
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List
from dacite import Config
from datetime import datetime

from common import *


@dataclass
class StatisticClosed(ModelBase):
    datetime: datetime
    volume: int
    min_price: float
    max_price: float
    open_price: float
    closed_price: float
    avg_price: float
    wa_price: float
    median: float
    moving_avg: Optional[float]
    donch_top: int
    donch_bot: int
    id: str
    mod_rank: Optional[int]


@dataclass
class StatisticLive(ModelBase):
    datetime: datetime
    volume: int
    min_price: float
    max_price: float
    avg_price: float
    wa_price: float
    median: float
    moving_avg: Optional[float]
    order_type: OrderType
    id: str
    mod_rank: Optional[int]


@dataclass
class Statistic:
    closed_48h: List[StatisticClosed]
    closed_90d: List[StatisticClosed]
    live_48h: List[StatisticLive]
    live_90d: List[StatisticLive]
