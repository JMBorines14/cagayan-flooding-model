from osgeo import gdal
from camodel import update_D
import numpy as np
import netCDF4 as nc
import sys

def x_coord(idx):
    return a*idx + b*idx + xoff

def y_coord(idx):
    return d*idx + e*idx + yoff

def simulation(L, D, I, depth_var, m, n):
    for time in range(1):
        #update R by calling update_R
        #update D
        I, ibabawas, idadagdag = update_D(L, D, I, m, n)
        D = D - ibabawas + idadagdag

        depth_var[time, :, :] = D
        L = S + D

#initialize the dataset
dataset = gdal.Open(sys.argv[1])
n, m, band = dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount
print(f'The size is {m} x {n}')
xoff, a, b, yoff, d, e = dataset.GetGeoTransform()

#initialize output file and dimensions
output_dataset = nc.Dataset('output.nc', 'w', format = 'NETCDF4')
time = output_dataset.createDimension('time', None)
lat = output_dataset.createDimension('lat', m)
lon = output_dataset.createDimension('lon', n)

times = output_dataset.createVariable('time', 'f8', ('time',))
lats = output_dataset.createVariable('lat', 'f4', ('lat',))
lons = output_dataset.createVariable('lon', 'f4', ('lon',))
depth = output_dataset.createVariable('depth', 'f4', ('time', 'lat', 'lon',))

#output latitudes and longitudes to the dataset
lats[:] = np.array([x_coord(k) for k in m])
lons[:] = np.array([y_coord(k) for k in n])

#get surface matrix
data1 = dataset.GetRasterBand(1).ReadAsArray()
S = np.array([list(i) for i in list(data1)])
dataset = None

#initialize rainfall matrix
R = np.zeros((m,n)) #rainfall
R[4093][4093] = 100

#define the I and D matrices
I = np.zeros((m,n)) #I_total
L = S
D = R

#call to simulation function
#simulation(C, L, D, I, depth, m, n)
output_dataset.close()