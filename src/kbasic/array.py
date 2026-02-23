# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from typing import Callable
from numpy import ndarray, argmin, any, abs, where, nanmean, nanmin, nanmax, linspace, nanstd, array, isnan, arange, mgrid
from scipy.interpolate import RegularGridInterpolator

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def tile(arr: ndarray) -> ndarray:
    """take an image and create a 3x3 grid of that image"""
    return np.r_[np.c_[arr, arr, arr], np.c_[arr, arr, arr], np.c_[arr, arr, arr]]
def where_closest(arr:ndarray, x): return int(argmin(abs(arr-x)))
def where_between(arr:ndarray, low, high): return where((arr>=low)&(arr<=high))
def bin_this(
        x, y, 
        n_bins: int = 50, 
        func: Callable = nanmean
) -> tuple[ndarray]:
    """a function to rebin x, y data and calculate errors.

    Args:
        x: the axis you want to bin
        y: the data associated with each bin
        n_bins (int, optional): desired number of bins. Defaults to 50.
        func (Callable, optional): the function to call on the members of each bin. Defaults to numpy.nanmean.

    Returns:
        x_binned (ndarray): the bins.
        y_binned (ndarray): func(members of each bin).
        bin_errors (ndarray): standard error of the mean for each bin
    """
    xbins = linspace(nanmin(x),nanmax(x),n_bins)
    Y,error = list(),list()
    for i,low_edge in enumerate(xbins[:-1]):
        high_edge = xbins[i+1]
        mask = (low_edge<x)&(x<high_edge)
        yin = y[mask]
        Y.append(func(yin))
        error.append(nanstd(yin)/sqrt(len(yin)))
    x_binned, y_binned, bin_errors = array(xbins)[:-1],array(Y),array(error)
    return x_binned, y_binned, bin_errors
def nan_clip(*args):
    """
    take a series of arrays and only return the indicies where ALL members are finite
    """
    mask = ~any([isnan(a) for a in args], axis=0)
    nanless_args = tuple([array(a)[mask] for a in args])
    return nanless_args
def interpolate2d(
        data, factor: int, 
        method: str = 'linear',
        periodic: bool = True
) -> ndarray:
    """interpolate 2d data on a regular grid by an even factor

    Args:
        data (ndarray[ndarray]): 2d data on a regular grid
        factor (int): how many new grid points per old grid points
        method (str, optional): the interpolation method. Defaults to 'linear'.

    Returns:
        ndarray[ndarray]: an interpolated grid of data
    """
    assert periodic, "non-periodic version not implemented yet! make one but be careful because the shapes will be awkward"
    Nx, Ny = array(data).shape
    grid = (arange(Nx+1), arange(Ny+1))
    data_repeat = np.zeros((Nx+1, Ny+1))
    data_repeat[:Nx, :Ny] = data 
    data_repeat[-1,:-1] = data[0]
    data_repeat[:-1,-1] = data[:,0]
    data_repeat[-1,-1] = data[-1,-1]
    new_grid = mgrid[:Nx:1/factor, :Ny:1/factor].T
    return RegularGridInterpolator(grid, data_repeat, method=method)(new_grid).T

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Decorators                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==