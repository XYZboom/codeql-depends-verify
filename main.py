import argparse
import csv
import json
from collections import defaultdict
from typing import List, Callable, Dict, Union, Set


def parse_args():
    _parser = argparse.ArgumentParser(description="Verify Depends by Codeql")
    _parser.add_argument('--depends-json', type=str, required=True, help='Depends json output path')
    _parser.add_argument('--codeql-csv', type=str, required=True, help='Codeql csv output path')
    _args = _parser.parse_args()
    return _args


class PredictAndParse:
    def __init__(self, _predict: Union[Callable[[str], bool], List[Callable[[str], bool]]],
                 _parse: Callable[[str], str]):
        self._predict = _predict
        self._parse = _parse
    
    def predict(self, _s: str) -> bool:
        if type(self._predict) is list:
            for _p in self._predict:
                if not _p(_s):
                    return False
            return True
        return self._predict(_s)
    
    def parse(self, _s: str) -> str:
        return self._parse(_s)


def handle(_s: str, _handlers: Dict[str, PredictAndParse]) -> Set[str]:
    _result = set()
    for _h in _handlers.values():
        if _h.predict(_s):
            _result.add(_h.parse(_s))
    return _result


def hardcoded_name_resolve(_name: str) -> Set[str]:
    _l = _name.split(".")
    
    def has_private(_s: str) -> bool:
        return "$private" in _s
    
    def is_getter(_s: str) -> bool:
        return _s.replace("$private", "").split(".")[-1].startswith("get")
    
    def is_setter(_s: str) -> bool:
        return _s.replace("$private", "").split(".")[-1].startswith("set")
    
    def getterBack0(_s: str) -> str:
        _s = _s.replace("$private", "")
        __l = _s.split(".")
        __l[-1] = __l[-1].replace("get", "")
        __l[-1] = __l[-1].replace(__l[-1][0], __l[-1][0].lower())
        return ".".join(__l)
    
    def setterBack0(_s: str) -> str:
        _s = _s.replace("$private", "")
        __l = _s.split(".")
        __l[-1] = __l[-1].replace("set", "")
        __l[-1] = __l[-1].replace(__l[-1][0], __l[-1][0].lower())
        return ".".join(__l)

    def getterBack1(_s: str) -> str:
        _s = _s.replace("$private", "")
        __l = _s.split(".")
        __l[-1] = __l[-1].replace("get", "")
        __l[-1] = __l[-1].replace(__l[-1][0], __l[-1][0])
        return ".".join(__l)

    def setterBack1(_s: str) -> str:
        _s = _s.replace("$private", "")
        __l = _s.split(".")
        __l[-1] = __l[-1].replace("set", "")
        __l[-1] = __l[-1].replace(__l[-1][0], __l[-1][0])
        return ".".join(__l)

    def someEleContainsKt(_s: str) -> bool:
        return any((_i.endswith("Kt") for _i in _s.split(".")))
    
    def removeEleContainsKt(_s: str):
        _s = _s.replace("$", ".")
        return ".".join(filter(lambda _s1: not _s1.endswith("Kt"), _s.split(".")))
    
    def containsDollar(_s: str):
        return "$" in _s
    
    def removeStrBeforeDollar(_s: str):
        _result = []
        for _i in _s.split("."):
            _result.append(_i.split("$")[-1])
        return ".".join(_result)
    
    _handler = {
        "normal": PredictAndParse(lambda _: True, lambda _s: _s),
        # codeql uses Kt for class Name
        "removeKt": PredictAndParse(lambda _: True, lambda _s: _s.replace("Kt", "")),
        "removeKt1": PredictAndParse(someEleContainsKt, removeEleContainsKt),
        "remove str before $": PredictAndParse(containsDollar, removeStrBeforeDollar),
        # inner class or kotlin generated property method handle
        "$ to .": PredictAndParse(lambda _s: "$private" not in _s, lambda _s: _s.replace("$", ".")),
        "remove$private": PredictAndParse(has_private, lambda _s: _s.replace("$private", "")),
        "getterBack": PredictAndParse([has_private, is_getter], getterBack0),
        "getterBack1": PredictAndParse([has_private, is_getter], getterBack1),
        "setterBack": PredictAndParse([has_private, is_setter], setterBack0),
        "setterBack1": PredictAndParse([has_private, is_setter], setterBack1),
        "removeLast": PredictAndParse(lambda _: True, lambda _s: _s.replace(f".{_l[-1]}", "")),
        "addLast": PredictAndParse(lambda _: True, lambda _s: _s + f".{_l[-1]}"),
    }
    
    return handle(_name, _handler)


def toGetter(_name: str):
    return "get" + _name[0].upper() + _name[1:]


def toSetter(_name: str):
    return "set" + _name[0].upper() + _name[1:]


if __name__ == '__main__':
    args = parse_args()
    codeql = defaultdict(set)
    with open(args.codeql_csv) as f:
        reader = csv.reader(f)
        for r in reader:
            for i in r[3].splitlines():
                _li = i.split(" ")
                ori_src = _li[0]
                ori_dest = _li[1]
                srcs = hardcoded_name_resolve(ori_src)
                dests = hardcoded_name_resolve(ori_dest)
                for src in srcs:
                    for dest in dests:
                        name = f"{src} {dest}"
                        codeql[r[0]].add(name)
                        codeql["Use"].add(name)
                
    with open(args.depends_json) as f:
        depends = json.load(f)
    depends_vars = depends["variables"]
    depends_deps = depends["cells"]
    count = 0
    negative = 0
    positive = 0
    for dep in depends_deps:
        src = depends_vars[str(dep['src'])].split('|')[0]
        dest = depends_vars[str(dep['dest'])].split('|')[0]
        result = f"{src} {dest}"
        for t in dep['values']:
            count += 1
            if result in codeql[t]:
                negative += 1
            else:
                print(result, t)
                positive += 1
    
    print(negative / count)
    with open("debug.txt", "w") as f:
        f.write(str(codeql))