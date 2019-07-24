import numpy as np
import matplotlib.pyplot as plt
import glob
import xml.etree.ElementTree as ET
from pylab import cm

level = 0.3
fps = 1

# ------------------------------------------------------------------------------
# STEP I
# generate the RSET map for every random seed
# ------------------------------------------------------------------------------

print 'Step I: Generate the RSET map for every random seed...'

seeds = sorted(glob.glob('12*/corridor_traj.xml'))

for seed in seeds:

    seed_nr = int(seed[:4])
    print '\t\--> processing seed nr.', seed_nr

    traj_xml = ET.parse( seed )
    traj_root = traj_xml.getroot()

    # Setup RSET map
    delta = 0.6
    x = np.arange(0, 30+0.01, delta)
    y = np.arange(0, 10.2+0.01, delta)
    rset_map = np.zeros((len(y), len(x)))
    rset_map_glob = np.zeros((len(y), len(x)))
    rset_map[:] = np.nan

    cmap = cm.get_cmap('RdYlGn_r', 10)

    for frame in traj_root.findall('./frame')[::1]:
        frame_id = int( frame.attrib['ID'] )
        #print frame_id

        for agent in frame.findall('agent'):

            if float(agent.attrib['z']) == level:
                agent_x, agent_y = float(agent.attrib['x']), float(agent.attrib['y'])

            if frame_id % fps == 0:  # only each full second (for higer fps)
                ix = (np.abs(x-agent_x)).argmin()
                iy = (np.abs(y-agent_y)).argmin()
                rset_map[iy,ix] = frame_id/fps

    plt.close()
    fig = plt.figure(figsize=(8 , 4.5))
    ax1 = fig.add_subplot(111)
    ax1.set_aspect('equal')

    ax1.set_title('RSET map seed nr. %i'%seed_nr)

    # plot the room
    ax1.plot([0,0], [0,10.2], c='grey', lw=15)
    ax1.plot([0,30], [10.2,10.2], c='grey', lw=15)
    ax1.plot([0,30], [0,0], c='grey', lw=15)
    ax1.plot([30,30], [0,7.5], c='grey', lw=15)
    ax1.plot([30,30], [9.5,10], c='grey', lw=15)

    aa = ax1.pcolorfast(x, y, rset_map, vmin=0, vmax=100, cmap=cmap)
    col = plt.colorbar(aa, ticks=np.arange(0,101,10), label='RSET in s', orientation='horizontal')

    np.savetxt('%i/rset_map_%i.txt'%(seed_nr, seed_nr), rset_map)

    ax1.set_xlabel('x in m')
    ax1.set_ylabel('y in m')
    ax1.set_xlim(0,30)
    ax1.set_ylim(0,10)
    fig.set_tight_layout(True)

    plt.savefig('%i/rset_map_%i.png'%(seed_nr, seed_nr), dpi=300)

# ------------------------------------------------------------------------------
# STEP II
# generate the RSET map for all random seeds
# ------------------------------------------------------------------------------

print 'Step II: Generate the RSET map for all random seeds...'

rset_maps = sorted(glob.glob('12??/rset_map_12*.txt'))

# Setup RSET map
delta = 0.6
x = np.arange(0, 30+0.01, delta)
y = np.arange(0, 10.2+0.01, delta)

percentile = 95
rset_map_tuple = ()

for rset in rset_maps:

    seed_nr = int(rset[:4])
    print '\t\--> processing seed nr.', seed_nr

    rset_map_tuple +=  (np.loadtxt(rset),)

    rset_stack = np.dstack(rset_map_tuple)
    rset_percentiles = np.zeros((np.shape(rset_stack)[0], np.shape(rset_stack)[1]))

    for i, row in enumerate(rset_stack):
        for j, col in enumerate(row):
            rset_percentiles[i,j] = np.nanpercentile(rset_stack[i,j, :], percentile)

cmap = cm.get_cmap('RdYlGn_r', 12)

fig = plt.figure(figsize=(8,5))
ax1 = fig.add_subplot(111)
ax1.set_aspect('equal')

ax1.set_title('RSET, 10 Realisations')

# plot the room
ax1.plot([0,0], [0,10.2], c='grey', lw=15)
ax1.plot([0,30], [10.2,10.2], c='grey', lw=15)
ax1.plot([0,30], [0,0], c='grey', lw=15)
ax1.plot([30,30], [0,7.5], c='grey', lw=15)
ax1.plot([30,30], [9.5,10], c='grey', lw=15)

aa = ax1.pcolorfast(x, y, rset_percentiles, vmin=0, vmax=120, cmap=cmap)
col = plt.colorbar(aa, ticks=np.arange(0,121,20), label='RSET in s', orientation='horizontal')

ax1.set_xlabel('x in m')
ax1.set_ylabel('y in m')
ax1.set_xlim(0,30)
ax1.set_ylim(0,10.2)
fig.set_tight_layout(True)

# save RSET map as plot
plt.savefig('RSET_map_all_seeds.png')

# save RSET map as txt
np.savetxt('RSET_map_all_seeds.txt', rset_percentiles)
