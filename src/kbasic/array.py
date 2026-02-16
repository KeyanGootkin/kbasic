from numpy import ndarray, argmin, abs, where, nanmean, nanmin, nanmax, linspace, nanstd, array, isnan, arange, mgrid
from scipy.interpolate import RegularGridInterpolator

def where_closest(arr:ndarray, x): return int(argmin(abs(arr-x)))
def where_between(arr:ndarray, low, high): return where((arr>=low)&(arr<=high))

def bin_this(x, y, n_bins=50, func=nanmean):
    xbins = linspace(nanmin(x),nanmax(x),n_bins)
    Y,error = list(),list()
    for i,low_edge in enumerate(xbins[:-1]):
        high_edge = xbins[i+1]
        mask = (low_edge<x)&(x<high_edge)
        yin = y[mask]
        Y.append(func(yin))
        error.append(nanstd(yin)/sqrt(len(yin)))
    return array(xbins)[:-1],array(Y),array(error)

def nan_clip(*args):
    mask = ~any([isnan(a) for a in args], axis=0)
    nanless_args = tuple([array(a)[mask] for a in args])
    return nanless_args

def interpolate2d(data, factor, method='cubic'):
    Nx, Ny = array(data).shape
    return RegularGridInterpolator((arange(Nx), arange(Ny)), data, method=method)(mgrid[:Nx-1:1/factor, :Ny-1:1/factor].T).T