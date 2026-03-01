from __future__ import annotations

from ..Components.Component import Clock
from ..Components.Component import TimeComponent

from ..Components.Signal import SourceModule

from ..Constants import RND_GEN

class RandomNumSource(TimeComponent):
    def __init__(self, source_module: SourceModule|None = None, num_range: int = 2, name: str= "default_random_num_source"):
        super().__init__(name)
        self.num: int = 0

        self._num_range = num_range
        self._source_module = source_module

    def simulate(self, clock: Clock):
        if(self._source_module):
            self.num = self._source_module(clock)
        else:
            self.num = int(RND_GEN.integers(0, self._num_range))

    def output_port(self, kwargs: dict = {}):
        #return super().output_port(kwargs)
        kwargs['num'] = self.num
        return kwargs