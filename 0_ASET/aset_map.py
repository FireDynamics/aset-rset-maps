import numpy as np
import matplotlib.pyplot as plt
from pylab import cm
import glob
from PIL import Image
import slice_reader

aset_quantity = "SOOT EXTINCTION COEFFICIENT"
aset_quantity_height = 2.0

# ------------------------------------------------------------------------------
# STEP I
# convert FDS slicefiles to ascii files
# ------------------------------------------------------------------------------

print("Step I: Read FDS slicefiles...")

data_root = "HRR_60kW"
smv_file_name = "ASET_animation.smv"
meshes = slice_reader.readMeshes(data_root + '/' + smv_file_name)
slice_infos = slice_reader.readSliceInfos(data_root + '/' + smv_file_name)

print("slice files found:")
for s in slice_infos:
    print(s.infoString())

# choose only the extinction coefficient slice
slice_extinction = slice_reader.findSlices(slice_infos, meshes, aset_quantity, 2, aset_quantity_height)[0]
slice_extinction.readAllTimes(data_root)
slice_extinction.readData(data_root)
slice_extinction.mapData(meshes)
print(slice_extinction.times)

slice_times = slice_extinction.times
slice_data = slice_extinction.sd
slice_xs = slice_extinction.sm.mesh[0]
slice_ys = slice_extinction.sm.mesh[1]

print(slice_xs, slice_ys)

it = 5
for iy in range(slice_data[it].shape[1]):
    for ix in range(slice_data[it].shape[0]):
        print(ix, iy, slice_xs[ix,iy], slice_ys[ix,iy], slice_data[it][ix,iy])
        nix = round(slice_xs[ix,iy] / 0.6)
        niy = round(slice_ys[ix,iy] / 0.6)
        print(nix, niy)

# ------------------------------------------------------------------------------
# STEP II
# generate the ASET map from FDS slicefiles
# ------------------------------------------------------------------------------

print("Step II: Generate the ASET map from FDS slicefiles...")

# quantities of interest (the dictionary includes the threshold as well)
quantities = {'extinction':0.23}

# Setup ASET map (floor of 30 m x 10 m)
# define floor elements' extension in meters
delta = 0.6
# define floor elements' centers
x = np.arange(delta/2, 30, delta)
y = np.arange(delta/2, 10, delta)

# create an empty map with a maximal ASET of 120 seconds
aset_map = np.zeros((len(y), len(x)))
aset_map[:] = 120

aset_map_glob = np.zeros_like(aset_map)
aset_map_glob[:] = 120

cmap = cm.get_cmap('RdYlGn', 12)
cmap_g = cm.get_cmap('Greys')

for q in quantities:

    slices = glob.glob('HRR_60kW/ascii_slices/%s/*.txt'%q)
    slices = sorted(slices, key=lambda slice: int(slice[ slice.rfind('_')+1 : -4 ]) )

    for i, slice in enumerate(slices[:]):
        slice_nr = int(slice[slice.rfind('_')+1 : -4])
        print("\t --> ", slice)

        # load ascii slice file
        sf = np.loadtxt(slice, delimiter=' ')

        # interpolate slice file to ASET map resolution dx=0.2 m --> dx=0.6 m
        sf_interp = np.array(Image.fromarray(sf).resize((len(x), len(y))))#imresize(sf, np.shape(aset_map), interp='bilinear')
        # sf_interp.transpose()
        print(sf.shape, sf_interp.shape, aset_map.shape)

        # ASET map generation
        for j, row in enumerate(sf_interp):
            for k, cell in enumerate(row):
                # call the dictionary with the belonging threshold
                if cell >= quantities[q]:
                    aset_map[j,k] = slice_nr

        aset_map_glob = np.minimum(aset_map, aset_map_glob)

plt.close()
fig = plt.figure(figsize=(8 , 4.5))       # inch -> cm /2.54
ax1 = fig.add_subplot(111)
ax1.set_aspect('equal')

ax1.set_title('ASET')

# room
ax1.plot([0,0], [0,10.2], c='grey', lw=15)
ax1.plot([0,30], [10,10], c='grey', lw=15)
ax1.plot([0,30], [0,0], c='grey', lw=15)
ax1.plot([30,30], [0,7.5], c='grey', lw=15)
ax1.plot([30,30], [9.5,10], c='grey', lw=15)

aa = ax1.pcolorfast(x, y, aset_map_glob, vmin=0, vmax=120, alpha=0.8, cmap=cmap)
col = plt.colorbar(aa, ticks=np.arange(0,121,20), label='ASET in s', orientation='horizontal')

ax1.set_ylabel('y in m')
ax1.set_xlabel('x in m')

plt.xlim(0,30)
plt.ylim(0,10)

plt.tight_layout()

# save ASET map as plot
plt.savefig('ASET_map.png', dpi=300)

# save ASET map as txt
np.savetxt('ASET_map.txt', aset_map_glob)
