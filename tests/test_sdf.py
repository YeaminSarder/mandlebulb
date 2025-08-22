import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from pytest_check import check
from sdf import CircleSdf

def test_circle_sdf():
    circlesdf = CircleSdf(10)
    with check: assert circlesdf((0,0,0)) == -10
    with check: assert circlesdf((5,0,0)) == -5
    with check: assert circlesdf((10,0,0)) == 0
    with check: assert circlesdf((20,0,0)) == 10
    with check: assert circlesdf((0,5,0)) == -5
    with check: assert circlesdf((0,10,0)) == 0
    with check: assert circlesdf((0,20,0)) == 10
    with check: assert circlesdf((0,0,5)) == -5
    with check: assert circlesdf((0,0,10)) == 0
    with check: assert circlesdf((0,0,20)) == 10
    
