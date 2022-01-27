from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List
from dacite import Config

from common import *


@dataclass
class LangInItem(ModelBase):
    @dataclass
    class Drop:
        name: str
        link: Optional[str]

    item_name: str
    description: str
    wiki_link: Optional[str]
    drop: List[Drop]
