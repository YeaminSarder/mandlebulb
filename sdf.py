from myutils import *
class Sdf:
    def sdf(self, point):
        return 0
    def __call__(self, point):
        return self.sdf(point) 
    def getColor(self):
        "returns the color of the point of last sdf call"
        return (1,0,0)
    def getNormal(self, point):
        h = 0.0001;
        da = self.sdf(vec3_add(point, (h,-h,-h)))
        db = self.sdf(vec3_add(point, (-h,-h,h)))
        dc = self.sdf(vec3_add(point, (-h,h,-h)))
        dd = self.sdf(vec3_add(point, (h,h,h)))
        return normalize(
             da - db - dc + dd,
             -da - db + dc + dd,
             -da + db - dc + dd
        )

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
    def getColor(self):
        return (0,1,0)

import math
class MandleBulbSdf(Sdf):
    def __init__(self):
        self.color = [0,0,1]
        self.colortrap = [0,0,0]
    def getColor(self):
        return (self.colortrap[0],self.colortrap[1],0)
    def sdf(self, point, power=8, max_iter=12, bailout=2.0):
        x, y, z = point
        z_vec = [x, y, z]
        dr = 1.0
        r = 0.0
        self.colortrap[0] = math.inf
        self.colortrap[1] = math.inf
        for i in range(max_iter):
            x, y, z = z_vec
            r = math.sqrt(x*x + y*y + z*z)

            #Division by zero check
            if r < 1e-6:
                return -1.0  #inside fractal therefore negative distance

            if r > bailout:
                break

            theta = math.acos(z/r)
            phi = math.atan2(y, x)
            dr = pow(r, power - 1.0) * power * dr + 1.0

            zr = pow(r, power)
            theta *= power
            phi *= power

            z_vec = [
                zr * math.sin(theta) * math.cos(phi) + point[0],
                zr * math.sin(theta) * math.sin(phi) + point[1],
                zr * math.cos(theta) + point[2]
            ]
            self.colortrap[0] = min(self.colortrap[0], zr)
            self.colortrap[1] = min(self.colortrap[1],abs(z_vec[2]))
        return 0.5 * math.log(r) * r / dr if r > 0 else -1.0
