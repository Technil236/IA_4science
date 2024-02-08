# python3 code to open ncep2 mslp
import netCDF4 as nc
import matplotlib.pyplot as plt
import cftime
import numpy as np
import sklearn
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram


def subset(data,lat,lon,sub):
    ''' subdata, sublat, sublon = subset(data,lat,lon,sub)
    Simple function to subset data sub ((latmin,latmax),(lonmin,lonmax)) tuple
    '''
    lt1,lt2 = sub[0]; ln1,ln2 = sub[1]
    ilats = ((lt1<=lat) & (lat<=lt2)).nonzero()[0]
    ilons = ((ln1<=lon) & (lon<=ln2)).nonzero()[0]
    subdata = data[:,ilats[0]:ilats[-1]+1,ilons[0]:ilons[-1]+1]
    sublat=lat[ilats[0]:ilats[-1]+1];sublon=lon[ilons[0]:ilons[-1]+1]

    return subdata, sublat, sublon

def clustering_data (subset , clusters):



    return

datadir="/srv/local/Disk_Space/data/mlsp/"
mslpfile = datadir+'mslp.1979.nc'

ncf = nc.Dataset(mslpfile)
mslp = ncf.variables['mslp'][:].data
mslp = mslp/100 # convert from Pascals to hectoPascals
time = ncf.variables['time'][:].data
time_units = ncf.variables['time'].units
dtime_humans = cftime.num2date(time,time_units)
lat = ncf.variables['lat'][:].data
lon = ncf.variables['lon'][:].data
ncf.close()

latSN,lonWE = (-40,-10),(10,40)
sub = (latSN,lonWE)
mslpSA,latSA,lonSA = subset(mslp,lat,lon,sub)
xx, yy = np.meshgrid(lonSA,latSA)

chosendate = cftime.datetime(1979,2,6)
chosenhour = cftime.date2num(chosendate,time_units)
ixt = np.argmin(np.abs(time - chosenhour))

print(mslp.shape)

#plt.hist(mslpSA.ravel())
plt.figure(figsize=[8,9])
clevs=np.arange(1000,1040,1)
plt.contour(xx,yy,mslpSA[ixt,:,:],clevs)


print(mslp)
# plt.figure(figsize=[8,9])
# for ixt in range(len(time)):
#     plt.contour(xx,yy,mslpSA[ixt,:,:],clevs)
#     plt.draw()
#     plt.pause(1)
#     plt.clf()



def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

X = mslpSA.reshape((mslpSA.shape[0]),(mslpSA.shape[1]*mslpSA.shape[2]),order='F')
#X = mslpSA.reshape((mslpSA.shape[0],-1),order='F')
n_samples, n_features = X.shape
# setting distance_threshold=0 ensures we compute the full tree.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

model = model.fit(X)
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
plot_dendrogram(model, truncate_mode="level", p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()