from mandlebulb import mandelbulb_sdf

def test_points():
    #I have taken random sample points
    points=[
        (0, 0, 0),         # center 
        (1, 0, 0),         # near surface
        (2, 2, 2),         # outside fractal
        (0.5, -0.5, 0.5),  # inside region
        (10, 0, 0),        # far away
    ]

    for p in points:
        d=mandelbulb_sdf(p)
        print(f"Point {p} -> Distance {d:.6f}")

if __name__ == "__main__":
    test_points()