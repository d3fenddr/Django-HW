from models import CarCreate, CarRead
from In_memory_data import _next_id, _lock, _store

def _create_car(payload: CarCreate) -> CarRead:
    global _next_id
    with _lock:
        cid = _next_id
        _next_id += 1
        car = CarRead(id=cid, **payload.model_dump())
        _store[cid] = car
        return car

def _get_car_by_id(cid: int) -> CarRead:
    with _lock:
        car = _store.get(cid)
        if not car:
            raise KeyError(f"Car with id={cid} not found")
        return car

def _delete_car(cid: int):
    with _lock:
        if cid not in _store:
            raise KeyError(f"Car with id={cid} not found")
        del _store[cid]
