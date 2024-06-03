from collections import defaultdict
from typing import Dict, Tuple, List


class Statistician:
    __dict: Dict[str, List[int]]
    
    def __init__(self):
        self.__dict = defaultdict(lambda: [0, 0])
    
    def __str__(self):
        _result = ""
        for i in self.__dict:
            _negative, _positive, = self.__dict[i]
            _result += f"{i}: {_negative / (_positive + _negative)}\n"
        return _result
    
    def negative(self, _s: str):
        self.__dict[_s][0] += 1
    
    def positive(self, _s: str):
        self.__dict[_s][1] += 1
