# pylint: skip-file
import pytest
from kbasic.array import tile, where_closest, where_between, bin_this, nan_clip, only_finite,\
    interpolate2d, kspec, kspec1d, kspec3d
import numpy as np

def test_main():
    assert np.all(tile(np.ones((3,3)))==np.ones((9,9)))
    assert where_closest(range(10), 2.1)==2
    assert np.all(where_between(range(10), 1, 5)[0]==[1, 2, 3, 4, 5])
    x_binned, y_binned, y_bin_errors = bin_this(range(10), np.ones(10), n_bins=4)
    assert all(x_binned == [0, 3, 6])
    assert all(y_binned == [1, 1, 1])
    assert all(y_bin_errors == [0, 0, 0])
    assert nan_clip([np.nan, 1, 2], [0, np.nan, 2])==([2,], [2,])
    assert only_finite([np.inf, 1, 2], [0, np.nan, 2])==([2,], [2,])
    assert np.all(interpolate2d(np.ones((10,10)), 2)==np.ones((20,20)))
    x = np.zeros((10,10))
    x[5,5]=1
    assert np.all(kspec(np.ones((10,10)))==x)
    assert kspec1d(np.ones((10,10)), return_bin_edges=True, bins=5)[0][0]==0
    assert kspec1d(np.sin(2*(np.mgrid[:100,:100])[1]/(2*np.pi)), bins=5)[1].argmax()==1
    x = np.zeros((7, 5))
    x[0,0] = 1
    assert np.all(kspec3d(np.ones((10,10,10)))[2]==pytest.approx(x))