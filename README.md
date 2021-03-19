# FWHM from KDE peak

A quick estimate of the upper/lower bounds and FWHM of a KDE peak


```python
import numpy as np
from matplotlib import pyplot as plt

import fwhm_from_kde as ffkde
```

# Generate some test data and plot it


```python
np.random.seed(42)
x = np.append(np.random.normal(1900, 100, size=10000),
              np.random.normal(2120, 100, size=5000))
print(x.shape)

fig,ax = plt.subplots()

_ = ax.hist(x, bins=60)
```

    (15000,)



    
![png](docs/output_3_1.png)
    


# Calculate the FWHM of the KDE peak

## Use the auto plotting feature


```python
_,_,_,_,_ = ffkde.fwhm_from_kde(x, show=True)
```

    KDE estimation with Gaussian kernel width = 15.919
    KDE peak = 1916.009 +235.197, -130.984



    
![png](docs/output_5_1.png)
    


# Plot the result manually


```python
peak, fwhm, hwhm_upp, hwhm_low, kde_xy = ffkde.fwhm_from_kde(x, show=False)

label = r'X = {:.3f} $^{{+{:.3f}}}_{{-{:.3f}}}$'.format(
    peak,hwhm_upp-peak,peak-hwhm_low)

fig,ax = plt.subplots()
_ = ax.hist(x, bins=60, color='grey', alpha =.5)
ax.axvline(peak, color='C0')
ax.axvline(hwhm_low, color='C0')
ax.axvline(hwhm_upp, color='C0')
ax.hlines(kde_xy[1][kde_xy[1].argmax()]/2, 
          hwhm_low, hwhm_upp, color='C1')
ax.plot(kde_xy[0], kde_xy[1], '-', color='C0')
ax.text(ax.get_xlim()[0],
        ax.get_ylim()[1]*1.1, '{:s}'.format(label), color='C0')
ax.set_xlabel('X')
ax.set_ylabel('N')

```

    KDE estimation with Gaussian kernel width = 15.919
    KDE peak = 1916.009 +235.197, -130.984





    Text(0, 0.5, 'N')




    
![png](docs/output_7_2.png)
    


---------

# Use some other test data

Load test data


```python
import pickle
filename = 'test/data/N_tot_MC_smaple_OMP_R.pickle'
filename = 'test/data/N_tot_MC_smaple_All.pickle'
with open(filename, 'rb') as f:
    x = pickle.load(f)
```

Print basic stats


```python
print('len = {:}, min = {:.2f}, max = {:.2f}\n 16%,50%,84% = {:}\n std_mean = {:}\
'.format(len(x), x.min(), x.max(), np.percentile(x,[15.9,50,84.1]), 
         x.std()/np.sqrt(len(x))
                                                                       )
     )
```

    len = 10000, min = 128.75, max = 253418.62
     16%,50%,84% = [  990.73092484  3579.07433514 17294.38213141]
     std_mean = 167.9843211320867


Plot it


```python
_ = plt.hist(x[x<6000],bins=100)
```


    
![png](docs/output_15_0.png)
    


Analyse it with fwhm_from_kde


```python

_,_,_,_,_ = ffkde.fwhm_from_kde(x[x<6000], nbins=100, show=True)

```

    KDE estimation with Gaussian kernel width = 58.707
    KDE peak = 816.313 +611.168, -229.188



    
![png](docs/output_17_1.png)
    



```python

```
