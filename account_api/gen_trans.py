import sys
import pprint
lines = sys.stdin.readlines()
dct = {}
for line in lines:
    key = line.split()[0]
    trans = line.split('\'')[1]
    dct[key] = trans


pprint.pprint(dct)