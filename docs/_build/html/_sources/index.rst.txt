.. KDE peak properties (kdepeakprops) documentation master file, created by
   sphinx-quickstart on Wed Mar 24 17:43:18 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to kdepeakprops's documentation!
==============================================================

Brief description
-----------------

A module to get some basic properties of a KDE peak: peak location, FWHM
and its upper and lower bounds. The KDE is estimated with
sklearn.neighbors.KernelDensity.

``kdepeakprops.kde_props`` takes a 1D array of values and returns an array
with the KDE peak properties (value, FWHM, upp, low) and another (2D
array) with the KDE samples.

.. image:: output_5_1.png

Contents
===================

.. toctree::
   :maxdepth: 4
   :caption: Contents:
   
   example.rst

Install
===================

``cd /path/to/install/dir``

``git clone https://github.com/iskren-y-g/kdepeakprops.git``
    
Add path or

.. code:: ipython3

    import sys
    sys.path.insert(0,'/path/to/install/dir')</code>


API main
===================
.. automodule:: kdepeakprops.kdepeakprops
   :members:    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
