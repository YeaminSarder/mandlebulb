from myutils import *

def raymerch(point, direction, minsdf, max_iteration = 100, min_d = 0.00001, max_d = 1000):
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
        if safe_forward_distance < min_d:
            break
        d += safe_forward_distance
        if d > max_d:
            return vec3_sub(point, di) # point - di
        p = vec3_add(point, vec3_scaler_mul(d, di)) # point + d*di
        i += 1
    return vec3_add(point, vec3_scaler_mul(d, di)) # point + d*di

def raygen(x,y,z,a,b,c,p,q,r,resx=50,resy=50):
    """
    generate rays. yields raydirections based on
    camera position: (x,y,z)
    look at target: (a,b,c) and
    up vector: (p,q,r)
    """
    mid = normalize(*vec3_sub((a,b,c), (x,y,z)))
    v = (p,q,r)
    dy = normalize(*vec3_sub(v,vec3_scaler_mul(vec3_dot(mid, (p,q,r)),mid)))
    dx = vec3_cross(mid,dy)
    for i in range(resy):
        for j in range(resx):
            fy = -0.5 + i/resy
            fx = -0.5 + j/resx
            yield normalize(*vec3_add(vec3_add(mid, vec3_scaler_mul(fx,dx)),vec3_scaler_mul(fy,dy)))
