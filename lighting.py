from myutils import *


class LightSource:
    def __init__(self, loc):
        self.loc = loc
class Lighting:
    def __init__(self, ambient = (0.25,0.25,0.25), diffuse = 1):
        self.ambient = ambient
        self.diffuse = diffuse
        self.light_sources = []
    def addLightSource(self, lightSource):
        self.light_sources.append(lightSource)
    def get(self,point,normal,viewer):
        a = self.ambient
        d = 0
        for ls in self.light_sources:
            dd = vec3_dot(normalize(*vec3_sub(ls.loc, point)), normal);
            if dd >= 0:
                d += dd
        d = min(1,d)
        return vec3_add(a,(d,d,d)) 
