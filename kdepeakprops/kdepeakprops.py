#!/usr/bin/env python
# coding: utf-8
# Licensed under a 3-clause BSD style license - see LICENSE

"""
A module to get some basic properties of a KDE peak.
=================================================
"""

__author__ = "Iskren Y. Georgiev"

# Importing modules

import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
for axticks in ['xtick','ytick']:
    plt.rcParams['{:}.direction'.format(axticks)] = 'in'
    plt.rcParams['{:}.minor.visible'.format(axticks)] = True

from sklearn.neighbors import KernelDensity

__all__ = ['kde_props'] #, 'plot_func']

def kde_props(x, nbins = 'doane', n_samples = 1000, show = False):

    """    
    
    Estimation of KDE peak properties: FWHM and its upper and lower
    bounds. It uses the scikit-learn KDE estimator.

    Parameters
    ----------
        x: array_like
            The 1D data array.
        
        nbins: int or str, default: 'doane'
            Number of bins to generate histogram and scale the KDE cernel. 
            If a str, it must be one of the numpy.histogram_bin_edges bin
            calculation algorithms: auto, fd, doane, scott, stone,
            rice, sturges, sqrt.
            
            Details in numpy.histogram_bin_edges:
            https://numpy.org/doc/stable/reference/generated/numpy.histogram_bin_edges.html.
            
        n_samples: int, default: 1000
            Number of samples for the KDE
            
        show: bool, default: False
            Plot the result

    Returns
    -------
        kde_peak_prop: 1D array
            The properties of the KDE peak value, FWHM, upper and lower bounds.
            
        kde_xy: 2D array
            The KDE samples for manual plotting.

    """

    X = x[:,None]
    
    # Check if nbins is a string
    if isinstance(nbins, str):
        print('Using \'{:}\' metod '.format(nbins), end='')
        nbins = np.histogram_bin_edges(x, bins=nbins).shape[0]
        print('to diplay {:} bins.'.format(nbins))
    
    # For scaling and plotting purposes, estimate the kernel width.
    # TODO: make it an optional input so that one can set it.
    kde_kernelwidth = (np.nanmax(X)-np.nanmin(X))/nbins

    print('KDE estimation with Gaussian kernel width = {:.3f}'.format(kde_kernelwidth))
    kde = KernelDensity(kernel='gaussian', bandwidth=kde_kernelwidth).fit(X)

    samples_kde = np.linspace(X.min(),X.max(),n_samples)
    log_dens_kde = kde.score_samples(samples_kde[:,None])

    samp_d = (X.max()-X.min())/n_samples

    kde_xy = np.array([samples_kde,
                       np.exp(log_dens_kde) * len(X) *
                       samp_d * (n_samples/nbins)]
                     )

    print('KDE peak = ', end ='')
    kde_y_max = np.nanmax(kde_xy[1])
    kde_peak = kde_xy[0][kde_xy[1].argmax()]

    try:        
        kde_y_halfmax = kde_y_max/2.
        fwhm_low = (np.abs(kde_xy[1][:kde_xy[1].argmax()] - kde_y_halfmax)).argmin()
        fwhm_upp = (np.abs(kde_xy[1][kde_xy[1].argmax():] - kde_y_halfmax)).argmin() + kde_xy[1].argmax()
        hwhm_peak_kde_low = kde_xy[0][fwhm_low]
        hwhm_peak_kde_upp = kde_xy[0][fwhm_upp]
        fwhm_peak_kde = hwhm_peak_kde_upp - hwhm_peak_kde_low

    except:
        print("Warning! FWHM was not calculated")
        kde_peak = 0; hwhm_peak_kde_upp = 0 ; hwhm_peak_kde_low = 0

    print('{:.3f} +{:.3f}, -{:.3f}'.format(kde_peak,hwhm_peak_kde_upp-kde_peak,
                                           kde_peak-hwhm_peak_kde_low))
    dim_par_lab = r'X = {:.3f} $^{{+{:.3f}}}_{{-{:.3f}}}$, FWHM={:.3f}'.format(
        kde_peak, hwhm_peak_kde_upp-kde_peak, kde_peak-hwhm_peak_kde_low, 
        fwhm_peak_kde)

    if show:
        fig,ax = plt.subplots()
        bins = ax.hist(x, bins=nbins, color='grey', alpha =.5)
        ax.axvline(kde_peak, color='C0')
        ax.axvline(hwhm_peak_kde_low, color='C0')
        ax.axvline(hwhm_peak_kde_upp, color='C0')
        ax.hlines(kde_y_halfmax, hwhm_peak_kde_low, 
                  hwhm_peak_kde_upp, color='C1')
        ax.plot(kde_xy[0], kde_xy[1], '-', color='C0')
        ax.text(ax.get_xlim()[0],
                ax.get_ylim()[1]*1.1, '{:s}'.format(dim_par_lab), color='C0')
        ax.set_xlabel('X')
        ax.set_ylabel('N')
        #ax.set_xlim(0,6000)
        plt.show()
        
    kde_stats = np.empty(4)
    kde_stats = (kde_peak,fwhm_peak_kde,hwhm_peak_kde_upp,hwhm_peak_kde_low)

    return kde_stats,kde_xy
