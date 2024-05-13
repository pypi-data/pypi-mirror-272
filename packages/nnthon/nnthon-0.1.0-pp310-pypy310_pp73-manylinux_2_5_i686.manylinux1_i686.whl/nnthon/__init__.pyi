from typing import final

__all__ = ["SnowFlakeID"]

@final
class SnowFlakeID:
    def __init__(self, worker_id: int):
        self.worker_id: int

    def reset(self): ...
    def new_id(self) -> int: ...
