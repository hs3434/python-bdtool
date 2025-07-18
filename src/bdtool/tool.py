from string import Formatter
import sys

def get_formatter_keys(ss: str):
    res = set()
    for t in Formatter().parse(ss):
        if t[1] is not None:
            res.add(t[1])
    return res

def touch():
    with open(sys.argv[1], 'a') as f:
        pass