#!/usr/bin/env python3

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

K2MFF_LAT = 40.9080035
K2MFF_LON = -74.9245285

BAND_LIST = ['10m', '12m', '15m', '17m', '20m', '30m', '40m', '60m', '80m', '160m']
    
norm = matplotlib.colors.Normalize(vmin=0, vmax=50)
cmap = plt.get_cmap('jet')

from hamsci import geopack
from pyporktools.qrz import QRZSession

rbn_spots         = pd.read_csv('20170723.csv', header=0, usecols=['callsign', 'dx', 'band'])
rbn_spots_located = pd.read_csv('20170723_located.csv', index_col=0, header=0)

# Append the located values onto the 
rbn_spots = rbn_spots.assign(db=rbn_spots_located.db).assign(dx_lat=rbn_spots_located.dx_lat).assign(dx_lon=rbn_spots_located.dx_lon)
rbn_spots = rbn_spots.loc[rbn_spots.db.notnull()].loc[rbn_spots.dx_lat.notnull()].loc[rbn_spots.dx_lon.notnull()]

groups = rbn_spots.groupby(['band', 'callsign'])

k2mff2_counts = np.zeros(len(BAND_LIST))
k2mff3_counts = np.zeros(len(BAND_LIST))

for idx, band in enumerate(BAND_LIST):
    try:
        df = groups.get_group((band, 'K2MFF-2'))
        k2mff2_counts[idx] = df.shape[0]
    except KeyError as e:
        print('Key Error: {}'.format(e))
        
    try:
        df = groups.get_group((band, 'K2MFF-3'))
        k2mff3_counts[idx] = df.shape[0]
    except KeyError as e:
        print('Key Error: {}'.format(e))

f, ax = plt.subplots(figsize=(16, 9))

bar_idx = np.arange(len(BAND_LIST))
bar_width = 0.35

k2mff2_bar = ax.bar(bar_idx, k2mff2_counts, bar_width)
k2mff3_bar = ax.bar(bar_idx + bar_width, k2mff3_counts, bar_width)

ax.set_yticks(np.arange(0, 375, 25))

ax.set_xticks(bar_idx + bar_width / 2)
ax.set_xticklabels(BAND_LIST)

ax.set_ylabel('# Spots')
ax.set_xlabel('Band')

ax.legend((k2mff2_bar[0], k2mff3_bar[0]), ('K2MFF-2', 'K2MFF-3'))
ax.yaxis.grid(True)

f.savefig('compare', bbox_inches='tight')
plt.close(f)
