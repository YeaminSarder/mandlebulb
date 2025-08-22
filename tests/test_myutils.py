import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from myutils import *
from pytest_check import check

def test_vec3_cross():
    with check: assert vec3_cross((3,-3,1),(4,9,2)) == (-15,-2,39)    
    with check: assert vec3_cross((3,-3,1),(-12,12,-4)) == (0,0,0)    
