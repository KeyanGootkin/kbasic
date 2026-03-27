# pylint: skip-file
import pytest
from kbasic.vectors import Vector, Norm, VectorBase, Quaternion, hamilton_product, R2, R3
from numpy import pi, array

large_number = 1e100
small_number = 1e-100

def test_single_vector():
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # Test basic initialization
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    v = Vector(1, 1, 1, 1)
    with pytest.raises(TypeError): Vector(['hello', 'hi'])
    with pytest.raises(TypeError): Vector("hello")
    assert Vector(v)==v
    assert repr(v) == 'Vector(1, 1, 1, 1)'
    assert len(v) == 1
    assert v.ndims == 4
    assert abs(v) == 2
    for component in v:
        assert component == 1
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # comparison
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    v2 = v + 1
    assert v2 == Vector(2, 2, 2, 2)
    assert v2 != 1
    assert v2 == v * 2
    assert v2 == Vector(4,4,4,4) / 2
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # arithmetic
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    x1 = Vector(1, 1, 1)
    x2 = Vector(2, 2, 2)
    # vector + vector
    assert (x1 - x2).y == -1
    assert (x1 + x2).z == 3
    assert (x1 * x2) == 3 * (2 * 1)
    # vector + number (including reverses)
    assert x1 + 1 == x2
    assert 1 + x1 == x2
    assert x2 - 1 == x1
    assert 1 - x1 == x1*0
    assert x1 * 2 == x2
    assert 2 * x1 == x2
    assert x2 / 2 == x1
    assert 2 / x2 == x1
    # the repr depends on the component types
    assert repr(Vector(4, 4, 4) / 2) != repr(x2)
    assert repr(Vector(4, 4, 4) // 2) == repr(x2)
    # vector + array
    assert x1 + [1, 1, 1] == x2
    assert x2 - [1, 1, 1] == x1
    assert repr(x1 * [1, 2, 3]) == 'Vector(1, 2, 3)'
    # need to make this a numpy array to get approx to work
    assert array((x1 / [1, 2, 3]).components) == pytest.approx(array(Vector(1,1/2,1/3).components))
    assert x1 // [1, 2, 3] == Vector(1, 0, 0)
    assert [1, 2, 3] // x2 == Vector(0, 1, 1)
    assert (2, 4, 6) / x2 == Vector(1, 2, 3)
    assert 10 // Vector(5, 5, 5) == x2
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # rotation and angules
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    xhat, yhat = Vector(1,0,0), Vector(0,1,0)
    zhat = xhat.cross(yhat)
    assert zhat.z == 1
    q1 = Quaternion(pi/2, (0, 0, 1))
    q2 = Quaternion(small_number, (1, 0, 0))
    # assert array(q1.components) * (q2.components) == Quaternion(0, (0, 1, 0))
    # need to do .rotate .from_spherical and Quaternions
    yhat = Vector(0, 1)
    xhat = Vector(1, 0)
    assert array(xhat.rotate(pi/2).components)==pytest.approx(array(yhat.components))
    assert array(R3.from_spherical(1, 0, pi/2).rotate(-pi/2, (0, 1, 0)).components)\
        ==pytest.approx(array(zhat.components))
        
def test_multi_vector():
    n = 100
    t = array(range(n))+1
    t_square = t**2
    t_two = t*2
    ones = array([1]*n)
    zeros = ones * 0
    a = Vector(t, zeros, zeros, zeros)
    b = Vector(t, t, t, t)
    assert a + b == Vector(t_two, t, t, t)
    assert a - b == array([zeros, -t, -t, -t])
    assert all(a * b == t_square) # dot product
    assert a / b == Vector(ones, zeros, zeros, zeros)
    assert a[0] == Vector(1, 0, 0, 0)
    assert a[0, 5] == [Vector(1, 0, 0, 0), Vector(6, 0, 0, 0)]
    assert a[:2] == [Vector(1, 0, 0, 0), Vector(2, 0, 0, 0)]
