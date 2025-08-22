import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from pytest_check import check
from raymerch import raymerch
from sdf import CircleSdf

def test_raymerch_circle_sdf():
    s = CircleSdf(5)
    with check: assert raymerch((-10,0,0), (1,0,0), s) == (-5,0,0)
    with check: assert raymerch((0,0,100), (0,0,-1), s) == (0,0,5)
    with check: assert raymerch((0,100,0), (0,-1,0), s) == (0,5,0)
