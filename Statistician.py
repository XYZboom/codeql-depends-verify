from collections import defaultdict
from typing import Dict, List


class Statistician:
    __dict: Dict[str, List[int]]
    
    def __init__(self):
        self.__dict = defaultdict(lambda: [0, 0])
    
    def __str__(self):
        _result = ""
        _all_count = 0
        _all_pos = 0
        for i in self.__dict:
            _positive, _negative, = self.__dict[i]
            _count = _positive + _negative
            _all_count += _count
            _all_pos += _positive
            _result += f"{i}: {_count} {_positive / _count}\n"
        _result += f"all: {_all_count} {_all_pos / _all_count}"
        return _result
    
    def negative(self, _s: str):
        self.__dict[_s][1] += 1
    
    def positive(self, _s: str):
        self.__dict[_s][0] += 1
