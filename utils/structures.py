from typing import List, Dict, Any, NamedTuple, Optional


class Player(NamedTuple):
    id: str
    full_name: str
    first_name: str
    last_name: str
    is_active: bool
