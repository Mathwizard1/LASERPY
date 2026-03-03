from __future__ import annotations

class LPQException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)