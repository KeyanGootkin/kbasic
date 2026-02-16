import pytest 
from kbasic.vectors import R2, Norm

def test_vector():
    assert (R2(1, 2)-R2(1, 4)).y==-2

def test_norm():
    assert abs(Norm(1000, 1000, 1000, 10000000))==1