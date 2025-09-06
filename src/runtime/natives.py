"""List of predefined functions and constants, as `METHODS` and `CONSTANTS`"""
from math import pi, e, floor, ceil, sin, cos, tan, sqrt

#TODO: fix the system so it doesn't allow float constants in programmer mode. 
# I may remove identifiers entirely in programmer mode, which will also allow for ABCDEF for hexadecimal

CONSTANTS = {
    "pi" : pi,
    "e" : e
}


def root(value, base):
    return value ** (1/base)

METHODS = {
    "abs" : abs,
    "floor" : floor,
    "ceil" : ceil,
    "sin" : sin,
    "cos" : cos,
    "tan" : tan,
    "root" : root,
    "sqrt" : sqrt
}