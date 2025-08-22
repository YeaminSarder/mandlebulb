def dist(x,y,z,a,b,c):
    x = x-a
    y = y-b
    z = z-c
    return (x*x + y*y + z*z) ** 0.5

def normalize(x,y,z):
    l = dist(x,y,z,0,0,0)
    return x/l, y/l, z/l

def vec3_add(v1,v2):
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]

def vec3_scaler_mul(k, v):
    return k * v[0], k * v[1], k * v[2]

def raymerch(point, direction, minsdf, max_iteration = 100, threshold = 0.00001):
    """
    point:tuple - 3d coordinate of point
    direction:tuple - 3d vector indicating direction of ray
    minsdf:function(point) - a function that returns minimum of all sdfs present in the scene.

    returns point or None - point where the ray intersects scene surface
    """
    
    p = point
    di = normalize(*direction)
    d = 0 # distance from initial point

    i = 0
    while (i < max_iteration):
        safe_forward_distance = minsdf(p)
        if safe_forward_distance < threshold:
            break
        d += safe_forward_distance
        p = vec3_add(point, vec3_scaler_mul(d, di)) # point + d*di
        i += 1
    return vec3_add(point, vec3_scaler_mul(d, di)) # point + d*di
