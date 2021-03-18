#!/usr/bin/env python
# coding: utf-8

# Importing modules

import sys,os, gzip
import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
for axticks in ['xtick','ytick']:
    plt.rcParams['{:}.direction'.format(axticks)] = 'in'
    plt.rcParams['{:}.minor.visible'.format(axticks)] = True

from sklearn.neighbors import KernelDensity



def fwhm_from_kde(x, nbins = 60, n_samples = 1000, show=True):
    
    """
    Estimate the fwhm (upper/lower) value(s) around the KDE peak
    """
    
    X = x[:,None]

    #nbins = 60 #len(X)
    kde_bin = (np.nanmax(X)-np.nanmin(X))/nbins

    print('KDE estimation with kde kernel = {:.3f}'.format(kde_bin))
    kde = KernelDensity(kernel='gaussian', bandwidth=kde_bin).fit(X)

    print('KDE scores')
    #n_samples = 100
    samples_kde = np.linspace(X.min(),X.max(),n_samples)
    log_dens_kde = kde.score_samples(samples_kde[:,None])

    samp_d = (X.max()-X.min())/n_samples

    kde_xy = np.array([samples_kde, np.exp(log_dens_kde) * len(X) * samp_d * (n_samples/nbins)])

    print('KDE peak = ', end ='')
    kde_y_max = np.nanmax(kde_xy[1])
    #kde_peak = kde_xy[0][kde_xy[1] == kde_xy[1].max()][0]
    kde_peak = kde_xy[0][kde_xy[1].argmax()]
    try:
        #ax = sns.kdeplot(np.random.rand(100))
        #kde_curve = ax.lines[0]
        #x = kde_curve.get_xdata()
        #y = kde_curve.get_ydata()
        #halfmax = y.max() / 2
        #maxpos = y.argmax()
        #leftpos = (np.abs(y[:maxpos] - halfmax)).argmin()
        #rightpos = (np.abs(y[maxpos:] - halfmax)).argmin() + maxpos
        #fullwidthathalfmax = x[rightpos] - x[leftpos]
        #ax.hlines(halfmax, x[leftpos], x[rightpos], color='crimson', ls=':')
        #ax.text(x[maxpos], halfmax, f'{fullwidthathalfmax:.3f}\n', color='crimson', ha='center', va='center')
        #ax.set_ylim(ymin=0)
        #plt.show()

        #fwhm_low = 2*kde_peak/(kde_peak*.98)
        #fwhm_upp = 2*kde_peak/(kde_peak*1.05)
        #fwhm_peak_kde = kde_xy[0][(kde_xy[1] > kde_y_max/fwhm_low) & (kde_xy[1] < kde_y_max/fwhm_upp)]
        #hwhm_peak_kde_low = kde_peak-fwhm_peak_kde.min()
        #hwhm_peak_kde_upp = fwhm_peak_kde.max()-kde_peak
        
        kde_y_halfmax = kde_y_max/2.
        fwhm_low = (np.abs(kde_xy[1][:kde_xy[1].argmax()] - kde_y_halfmax)).argmin()
        fwhm_upp = (np.abs(kde_xy[1][kde_xy[1].argmax():] - kde_y_halfmax)).argmin() + kde_xy[1].argmax()
        hwhm_peak_kde_low = kde_xy[0][fwhm_low]
        hwhm_peak_kde_upp = kde_xy[0][fwhm_upp]

    except:
        print("Warning! FWHM was not calculated")
        kde_peak = 0; hwhm_peak_kde_upp = 0 ; hwhm_peak_kde_low = 0
        
    print('{:.3f} +{:.3f}, -{:.3f}'.format(kde_peak,hwhm_peak_kde_upp,hwhm_peak_kde_low))
    dim_par_lab = r'X = {:.3f} $^{{+{:.3f}}}_{{-{:.3f}}}$'.format(kde_peak,hwhm_peak_kde_upp,abs(hwhm_peak_kde_low))
    
    if show:
        fig,ax = plt.subplots()
        bins = ax.hist(x, bins=nbins, color='grey', alpha =.5)
        ax.axvline(kde_peak, color='C0')
        ax.axvline(hwhm_peak_kde_low, color='C0') #kde_peak-abs(hwhm_peak_kde_low), 
        ax.axvline(hwhm_peak_kde_upp+kde_peak, color='C0')
        ax.plot(kde_xy[0], kde_xy[1], '-', color='C0')
        ax.text(kde_peak,
                ax.get_ylim()[1]*1.1, '{:s}'.format(dim_par_lab), color='C0')
        ax.set_xlabel('X')
        ax.set_ylabel('N')
        ax.set_xlim(0,6000)
        plt.show
    
    return kde_peak,hwhm_peak_kde_upp,abs(hwhm_peak_kde_low),kde_xy