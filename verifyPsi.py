import argparse
import json

from Statistician import Statistician
from main import handle, PredictAndParse


def parse_args():
    _parser = argparse.ArgumentParser(description="Verify Depends by Codeql")
    _parser.add_argument('--depends-json', type=str, required=True, help='Depends json output path')
    _parser.add_argument('--psi-json', type=str, required=True, help='PSI json output path')
    _args = _parser.parse_args()
    return _args


def hardcode_name_handle(_s: str):
    def containsCompanion(_s: str) -> bool:
        return ".Companion" in _s
    
    def removeCompanion(_s: str):
        _l = _s.split(".")
        _l.remove("Companion")
        return ".".join(_l)
    
    def isConstructorName(_s: str) -> bool:
        _l = _s.split(".")
        if len(_l) < 2:
            return False
        return _l[-1] == _l[-2]
    
    def constructor2Class(_s: str) -> str:
        _l = _s.split(".")[:-1]
        if "Companion" in _l:
            _l.remove("Companion")
        return ".".join(_l)
    
    def isPropertyOrFieldName(_s: str):
        _l = _s.split(".")
        if len(_l) < 2:
            return False
        # a.b.c.ClassA.field
        return len(_l[-2]) > 0 and _l[-2][0].isupper() \
               and len(_l[-1]) > 0 and _l[-1][0].islower()
    
    def removeLastEle(_s: str) -> str:
        _l = _s.split(".")[:-1]
        return ".".join(_l)
    
    def repeatLastEle(_s: str) -> str:
        _last = _s.split(".")[-1]
        return _s + "." + _last
    
    _handler = {
        "normal": PredictAndParse(lambda _: True, lambda _s: _s),
        "remove .Companion": PredictAndParse(containsCompanion, removeCompanion),
        "Constructor as Class name": PredictAndParse(isConstructorName, constructor2Class),
        "Remove last element": PredictAndParse(isPropertyOrFieldName, removeLastEle),
        "Repeat last element": PredictAndParse(lambda _: True, repeatLastEle),
    }
    return handle(_s, _handler)


if __name__ == '__main__':
    args = parse_args()
    psi = set()
    psi_nodes = dict()
    psi_debug = set()
    
    with open(args.depends_json, encoding='utf-8') as f:
        depends = json.load(f)
    with open(args.psi_json, encoding='utf-8') as f:
        psi_json = json.load(f)
    
    for node in psi_json["nodes"]:
        psi_nodes[node["id"]] = node["label"] \
            .replace(" (Not in project)", "") \
            .split("|")[0]
    for edge in psi_json["edges"]:
        ori_src = psi_nodes[edge["source"]]
        ori_dest = psi_nodes[edge["target"]]
        srcs = hardcode_name_handle(ori_src)
        dests = hardcode_name_handle(ori_dest)
        for src in srcs:
            for dest in dests:
                psi.add(src + " " + dest)
                psi_debug.add(src + " " + dest + " " + edge["label"])
    
    depends_vars = depends["variables"]
    depends_deps = depends["cells"]
    stat = Statistician()
    def handle_depends(_s: str):
        return _s.split('|')[0]\
            .replace("\\", "/")\
            .replace("`", "")
    for dep in depends_deps:
        src = handle_depends(depends_vars[str(dep['src'])])
        dest = handle_depends(depends_vars[str(dep['dest'])])
        result = f"{src} {dest}"
        for t in dep['values']:
            if result in psi:
                stat.positive(t)
            else:
                print(result, t)
                stat.negative(t)
    
    print(stat)
    with open("debug.txt", "w") as f:
        f.write(str(psi_debug))
