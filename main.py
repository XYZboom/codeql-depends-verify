import argparse
import csv
import json
from collections import defaultdict
from typing import List


def parse_args():
    _parser = argparse.ArgumentParser(description="Verify Depends by Codeql")
    _parser.add_argument('--depends-json', type=str, required=True, help='Depends json output path')
    _parser.add_argument('--codeql-csv', type=str, required=True, help='Codeql csv output path')
    _args = _parser.parse_args()
    return _args

def hardcoded_name_resolve(_name: str)-> List[str]:
    _l = _name.split(".")
    return [
        _name,
        # codeql uses Kt for class Name
        _name.replace("Kt", ""),
        # inner class handle
        _name.replace("$", "."),
        # remove last name
        # sometimes, codeql thinks a constructor (e.g. lib.ClassA.ClassA) calls a method
        # but depends thinks a class (lib.ClassA) calls a method
        _name.replace(f".{_l[-1]}", "")
    ]

if __name__ == '__main__':
    args = parse_args()
    codeql = defaultdict(set)
    with open(args.codeql_csv) as f:
        reader = csv.reader(f)
        for r in reader:
            for i in r[3].splitlines():
                for name in hardcoded_name_resolve(i):
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