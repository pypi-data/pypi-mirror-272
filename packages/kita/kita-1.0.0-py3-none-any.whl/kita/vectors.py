from .basic import *

class Vector:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z


class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

class c_Affix:
    def __init__(self, a_z:complex):
        self.a_z = a_z

class c_Point:
    def __init__(self, z:complex):
        self.z = z

def tupleVector(vector:Vector):
    return (vector.x, vector.y, vector.z)

def getVector(point_A:Point, point_B:Point):
    x = point_B.x - point_A.x
    y = point_B.y - point_A.y
    z = point_B.z - point_A.z
    return Vector(x,y,z)

def c_tupleAffix(c_affix:c_Affix):
    return (c_affix.a_z)

def c_getVector(z_A:c_Point, z_B:c_Point):
    return c_Affix(z_B.z-z_A.z)
