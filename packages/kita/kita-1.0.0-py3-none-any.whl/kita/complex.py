from .basic import *
from math import atan

def arg(z:complex):
    return atan(z.imag/z.real)

def module(z:complex):
    return sqrt((z.real)**2 + (z.imag)**2)

def conjugate(z:complex):
    return complex(z.real, -z.imag)