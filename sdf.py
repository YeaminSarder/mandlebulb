from myutils import *
class Sdf:
    def sdf(self, point):
        return 0
    def __call__(self, point):
        return self.sdf(point)

class CircleSdf(Sdf):
    def __init__(self,radius, position = (0,0,0)):
        self.position = position
        self.radius = radius
    def sdf(self, point):
        point = vec3_add(point, self.position)
        return length(*point) - self.radius

class CubeSdf(Sdf):
    def __init__(self,corner, position = (0,0,0)):
        self.corner = corner
        self.position = position
    def sdf(self, point):
        point = vec3_add(point, self.position)
        q = vec3_sub(vec3_op1(abs,point), self.corner)
        return length(*vec3_op2(max,q,(0,0,0))) + min(max(*q),0)
