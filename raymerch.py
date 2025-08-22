from myutils import *

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
