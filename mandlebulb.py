import math

def mandelbulb_sdf(point, power=8, max_iter=12, bailout=2.0):
    x, y, z = point
    z_vec = [x, y, z]
    dr = 1.0
    r = 0.0

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
    
    return 0.5 * math.log(r) * r / dr if r > 0 else -1.0
