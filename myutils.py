def dist(x,y,z,a,b,c):
    x = x-a
    y = y-b
    z = z-c
    return (x*x + y*y + z*z) ** 0.5

def normalize(x,y,z):
    l = dist(x,y,z,0,0,0)
    return x/l, y/l, z/l

def length(x,y,z):
    return (x*x + y*y + z*z)**0.5

def vec3_add(v1,v2):
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]

def vec3_sub(v1,v2):
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]


def vec3_op1(f,v1):
    return tuple(map(f, v1))


def vec3_op2(f,v1,v2):
    return f(v1[0],v2[0]), f(v1[1],v2[1]), f(v1[2],v2[2])


def vec3_scaler_mul(k, v):
    return k * v[0], k * v[1], k * v[2]

def vec3_dot(v1,v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def vec3_cross(v1,v2):
    a, b, c = v1
    d, e, f = v2
    return b*f - e*c, c*d - a*f, a*e - b*d
