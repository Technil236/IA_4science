import numpy as np
import netCDF4
import sklearn
import skimage
import matplotlib
import scipy


file_path = '/srv/local/Disk_Space/data/mlsp/mslp.1979.nc'
data = netCDF4.Dataset(file_path)