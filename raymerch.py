def raymerch(point, direction, minsdf):
    """
    point:tuple - 3d coordinate of point
    direction:tuple - 3d vector indicating direction of ray
    minsdf:function(point) - a function that returns minimum of all sdfs present in the scene.

    returns point or None - point where the ray intersects scene surface
    """
    
