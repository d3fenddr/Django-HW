from typing import Dict
from threading import Lock
from models import CarRead

_store: Dict[int, CarRead] = {}
_next_id: int = 1
_lock: Lock = Lock()
