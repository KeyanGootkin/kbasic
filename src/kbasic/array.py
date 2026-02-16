import numpy as np
from scipy.interpolate import RegularGridInterpolator

def where_closest(arr:np.ndarray, x): return np.argmin(np.abs(arr-x))
def where_between(arr:np.ndarray, low, high): return np.where((arr>=low)&(arr<=high))

def bin_this(x, y, n_bins=50, func=np.nanmean):
    xbins = np.linspace(np.nanmin(x),np.nanmax(x),n_bins)
    Y,error = list(),list()
    for i,low_edge in enumerate(xbins[:-1]):
        high_edge = xbins[i+1]
        mask = (low_edge<x)&(x<high_edge)
        yin = y[mask]
        Y.append(func(yin))
        error.append(np.nanstd(yin)/np.sqrt(len(yin)))
    return np.array(xbins)[:-1],np.array(Y),np.array(error)

def nan_clip(*args):
    mask = ~np.any([np.isnan(a) for a in args], axis=0)
    nanless_args = tuple([np.array(a)[mask] for a in args])
    return nanless_args

def interpolate2d(data, factor, method='cubic'):
    Nx, Ny = np.array(data).shape
    return RegularGridInterpolator((np.arange(Nx), np.arange(Ny)), data, method=method)(np.mgrid[:Nx-1:1/factor, :Ny-1:1/factor].T).T