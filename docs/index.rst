.. KDE peak properties (kdepeakprops) documentation master file, created by
   sphinx-quickstart on Wed Mar 24 17:43:18 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to kdepeakprops's documentation!
==============================================================

Brief description
===================
Estimation of KDE peak properties: FWHM and its upper and lower bounds.

It takes a 1D array of values and returns two arrays. One (1D array)
with the KDE peak properties (value,FWHM, upp, low) and another (2D
array) with the KDE samples.

.. image:: output_5_1.png

Contents
===================

.. toctree::
   :maxdepth: 4
   :caption: Contents:
   
   example.rst

API main
===================
.. automodule:: kdepeakprops.kdepeakprops
   :members:    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
