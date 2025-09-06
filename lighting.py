from myutils import *


class LightSource:
    def __init__(self, loc):
        self.loc = loc
class Lighting:
    def __init__(self, ambient = (0.25,0.25,0.25), diffuse = 1, shininess = 16):
        self.ambient = ambient
        self.diffuse = diffuse
        self.shininess = shininess
        self.light_sources = []
    def addLightSource(self, lightSource):
        self.light_sources.append(lightSource)
    def apply(self,point,color,normal,viewer):
        a = self.ambient
        d = 0
        s = 0
        for ls in self.light_sources:
            light_dir = normalize(*vec3_sub(ls.loc, point))
            reflect_dir = normalize(*vec3_sub(vec3_scaler_mul(2*vec3_dot(light_dir, normal), normal), light_dir)) # 2l.n * n - l
            dd = vec3_dot(light_dir, normal);
            if dd >= 0:
                d += dd
            ss = vec3_dot(reflect_dir, normalize(*viewer))
            if ss >= 0:
                s += ss**self.shininess
        d = min(1,d)
        s = min(1,s)
        ad = vec3_add(a,(d,d,d))
        cad = vec3_serial_mul(color, ad)
        return vec3_add(cad, (s,s,s))
