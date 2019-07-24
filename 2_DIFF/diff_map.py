#!/usr/bin/python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import cm

# ------------------------------------------------------------------------------
# STEP I
# generate the difference map
# ------------------------------------------------------------------------------


# Diff map information
delta = 0.6
x = np.arange(0, 30+0.01, delta)
y = np.arange(0, 10.2+0.01, delta)

# import corrsponding aset map
aset_map = np.loadtxt( '../0_ASET/ASET_map.txt' )

# import corrsponding rset map
rset_map = np.loadtxt( '../1_RSET/RSET_map_all_seeds.txt' )

# calculate ASET-RSET
diff_map = aset_map - rset_map

plt.close()
fig = plt.figure(figsize=(8 , 4.5))       # inch -> cm /2.54
ax1 = fig.add_subplot(111)

ax1.set_title('Difference map')

# plot the room
ax1.plot([0,0], [0,10.2], c='grey', lw=15)
ax1.plot([0,30], [10.2,10.2], c='grey', lw=15)
ax1.plot([0,30], [0,0], c='grey', lw=15)
ax1.plot([30,30], [0,7.5], c='grey', lw=15)
ax1.plot([30,30], [9.5,10], c='grey', lw=15)

# colorbar with contrastive limiting state ASET-RSET = 0
top = cm.get_cmap('cool_r', 120)
bottom = cm.get_cmap('autumn', 120)

newcolors = np.vstack((top(np.arange(0, 120, 20)),
                       bottom(np.arange(0, 120, 20))))
newcmp = matplotlib.colors.ListedColormap(newcolors, name='ASETvsRSET', N=12)

dd = ax1.pcolorfast(x, y, diff_map, vmin=-60, vmax=60, cmap=newcmp)
cb = plt.colorbar(dd, label='ASET-RSET in s', orientation='horizontal')

cb.set_ticks( np.arange(-120, 121, 20) )
cbar_ticks = cb.ax.get_xticklabels()
cbar_ticks[-1]='> 60'
cb.ax.set_yticklabels(  cbar_ticks )

ax1.set_xlabel('x in m')
ax1.set_ylabel('y in m')

ax1.set_aspect('equal')

plt.savefig('DIFF_map.png', dpi=300)

# save DIFF map as txt
np.savetxt('DIFF_map.txt', diff_map)


# ------------------------------------------------------------------------------
# STEP II
# process the difference map
# ------------------------------------------------------------------------------

# inspect the negative portion of the difference map histogram
diff_map_flat = diff_map.ravel()
freqs, bins = np.histogram(diff_map_flat[~np.isnan(diff_map_flat)], bins=np.arange(-120,0.01,20))

#calculate minimum ASET-RSET
print '\t\--> calculate minimum ASET-RSET...'
diff_min = np.nanmin(diff_map)
print '\tt_min = %i s'%diff_min

#calculate area, where ASET < RSET
print '\t\--> calculate area, where ASET < RSET...'
area = np.sum(freqs[np.where(freqs>0)])*delta**2
print '\tA = %i qm'%area

#calculate C (EMD)
print '\t\--> calculate C (EMD)...'
bin_centers_lt0 = bins[1:]-10
prod = freqs * bin_centers_lt0
EMD = np.sum(prod)*delta**2 #per square meters
print '\tC = %i s x qm'%EMD

plt.close()
fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
ax1.xaxis.set_tick_params(width=0)

ax1.hist(diff_map_flat[~np.isnan(diff_map_flat)], color='lightskyblue',\
    bins=np.arange(0,121,20), edgecolor='k' )

label = r'C = %i s $\times$ m$^2$'%(EMD)

ax1.hist(diff_map_flat[~np.isnan(diff_map_flat)], color='red', alpha=0.8,\
    bins=np.arange(-120,0.01,20), edgecolor='k', label=label )

ax1.set_xlabel('ASET-RSET in s')
ax1.set_ylabel('No. elements')
ax1.axvline(0, lw=2, ls='dashed', c='r')

ax1.set_xlim(-60,120)
ax1.set_ylim(0,450)

ax2 = ax1.twinx()
ax2.set_yticks(ax1.get_yticks()*delta**2)
ax2.set_ylabel(r'Area in m$^2$')
ax2.tick_params(axis='y')

ax1.legend()

plt.tight_layout()
plt.savefig('DIFF_map_hist.png', dpi=300)
