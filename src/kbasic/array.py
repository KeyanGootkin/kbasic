"""pure array operations"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from typing import Callable
from kbasic.typing import Number, ArrayLike, NDArray
from numpy import argmin, any, all, absolute, hypot, logspace, log10, where, \
                  nanmean, nanmin, nanmax, sqrt, linspace, nanstd, array, isnan, \
                  isfinite, arange, mgrid, r_, c_, zeros, delete, unravel_index
from numpy.fft import fftshift, fft2, fftn
from scipy.interpolate import RegularGridInterpolator
from tqdm import tqdm

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def tile(arr: ArrayLike) -> NDArray:
    """take an array and create a 3x3 grid of copies of that array
    
    Args:
        arr (ArrayLike): the 2D array you want a tiled version

    Returns:
        NDArray: a 3x3 grid of coppies of arr
    """
    x = array(arr)
    return r_[c_[x, x, x], c_[x, x, x], c_[x, x, x]]
def where_closest(arr:ArrayLike, value: Number) -> int | tuple[int]: 
    """find the index where arr is closest to the value of x

    Args:
        arr (ArrayLike): the array to search for the index in
        value (Number): the value you want to get close to

    Returns:
        _type_: _description_
    """
    arr = array(arr)
    indices = unravel_index(argmin(absolute(arr-value)), arr.shape)
    return indices if len(indices)>1 else indices[0]
def where_between(arr:ArrayLike, low: Number, high: Number) -> NDArray: 
    """Find the range of indicies where arr is between low and high

    Args:
        arr (ArrayLike): the array to search through
        low (Number): the lower edge of the range (inclusive)
        high (Number): the upper edge of the range (inclusive)

    Returns:
        NDArray: an array which is True at indices where low<=arr<=high, and False elsewhere
    """
    arr = array(arr)
    return where((arr>=low)&(arr<=high))
def bin_this(
        x: ArrayLike, y: ArrayLike, 
        n_bins: int = 50, 
        func: Callable = nanmean
    ) -> tuple[NDArray]:
    """a function to rebin x, y data and calculate errors.

    Args:
        x: the axis you want to bin
        y: the data associated with each bin
        n_bins (int, optional): desired number of bins. Defaults to 50.
        func (Callable, optional): the function to call on the members of each bin. Defaults to numpy.nanmean.

    Returns:
        x_binned (NDArray): the bins.
        y_binned (NDArray): func(members of each bin).
        bin_errors (NDArray): standard error of the mean for each bin
    """
    x, y = array(x), array(y)
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
def nan_clip(*args: tuple[ArrayLike]) -> tuple[ArrayLike]:
    """
    take a series of arrays and only return the indicies where ALL members are not nan
    """
    mask = ~any([isnan(a) for a in args], axis=0)
    nanless_args = tuple([array(a)[mask] for a in args])
    return nanless_args
def only_finite(*args: tuple[ArrayLike]) -> tuple[ArrayLike]:
    """
    take a series of arrays and only return the indicies where ALL members are finite
    """
    mask = all([isfinite(a) for a in args], axis=0)
    nanless_args = tuple([array(a)[mask] for a in args])
    return nanless_args
def interpolate2d(
        data: ArrayLike, factor: int, 
        method: str = 'linear',
        periodic: bool = True
    ) -> NDArray:
    """interpolate 2d data on a regular grid by an even factor

    Args:
        data (ArrayLike): 2d data on a regular grid
        factor (int): how many new grid points per old grid points
        method (str, optional): the interpolation method. Defaults to 'linear'.

    Returns:
        NDArray: an interpolated grid of data
    """
    assert periodic, "non-periodic version not implemented yet! make one but be careful because the shapes will be awkward"
    Nx, Ny = array(data).shape
    grid = (arange(Nx+1), arange(Ny+1))
    data_repeat = zeros((Nx+1, Ny+1))
    data_repeat[:Nx, :Ny] = data 
    data_repeat[-1,:-1] = data[0]
    data_repeat[:-1,-1] = data[:,0]
    data_repeat[-1,-1] = data[-1,-1]
    new_grid = mgrid[:Nx:1/factor, :Ny:1/factor].T
    return RegularGridInterpolator(grid, data_repeat, method=method)(new_grid).T
def kspec(image: ArrayLike) -> NDArray:
    """take 2d fft and center k=0 at the center point"""
    return absolute(fftshift(fft2(image) / (1. * image.shape[0] * image.shape[1])))**2
def kspec1d(
        image: ArrayLike, 
        bins: int = 100, 
        return_bin_edges: bool = False
    ) -> tuple[NDArray, NDArray, NDArray]:
    """Take a 2d image and turn it into a 1d fft

    Args:
        image (ArrayLike): the array to take the FFT of 
        bins (int, optional): number of k bins. Defaults to 100.
        return_bin_edges (bool, optional): if true return the bin edges, not just the k values. Defaults to False.

    Returns:
        tuple[NDArray, NDArray, NDArray]: 
    """
    k = kspec(image)
    Ny, Nx = image.shape
    kmag = hypot(*mgrid[
                     -Ny // 2: Ny // 2,
                     -Nx // 2: Nx // 2
                     ][::-1])
    kmin = nanmin(kmag[kmag != 0])
    kmax = nanmax(kmag)
    kgrid = r_[[0], logspace(log10(3*kmin), log10(kmax), bins)]
    kx = array([nanmean([kgrid[i], kgrid[i+1]]) for i in range(len(kgrid)-1)])
    ks = array([nanmean(k[where((kgrid[i] < kmag) & (kmag < kgrid[i+1]))]) for i in range(len(kgrid)-1)])
    kerr = array([nanstd(in_bin:=k[where((kgrid[i] < kmag) & (kmag < kgrid[i+1]))])/sqrt(len(in_bin)) for i in range(len(kgrid)-1)])
    if not return_bin_edges: return kx, ks, kerr
    return kgrid, kx, ks, kerr
def kspec3d(
        cube: ArrayLike,
        parallel_axis: int = 0
    ) -> tuple[NDArray]:
    """docstring"""
    # Set up parallel axis
    n_par = cube.shape[parallel_axis]
    parallel = arange(-(n_par//2), n_par//2+1)
    # Set up perpendicular axis
    n_perp = delete(cube.shape, parallel_axis)
    perp_mag = hypot(*mgrid[
        -n_perp[1]//2:n_perp[1]//2,
        -n_perp[0]//2:n_perp[0]//2
    ][::-1])
    perp_min = nanmin(perp_mag[perp_mag>0])
    perp_max = nanmax(perp_mag)
    perp_grid = arange(0, perp_max, perp_min)
    n_perp = len(perp_grid)
    perp = perp_grid + perp_min/2
    # Take Fourier transform
    F = array(absolute(fftshift(fftn(cube))/(cube.shape[0]*cube.shape[1]*cube.shape[2])))
    k = array([
            [
                sum(
                    F[j][where(
                        (perp_mag >= perp_grid[i]) & (perp_mag < perp_grid[i+1]),
                    )]
            ) for i in range(n_perp-1)
        ] for j in tqdm(range(n_par), position=1, total=n_par)
    ])
    return parallel[n_par//2:], perp, k.T[:, n_par//2:]
