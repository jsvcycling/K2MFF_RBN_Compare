#!/usr/bin/env python3

import numpy as np
import pandas as pd

K2MFF_LAT = 40.9080035
K2MFF_LON = -74.9245285

from hamsci import geopack
from pyporktools.qrz import QRZSession

rbn_spots         = pd.read_csv('20170723.csv', header=0, usecols=['callsign', 'dx'])
rbn_spots_located = pd.read_csv('20170723_located.csv', index_col=0, header=0)

# Append the located values onto the 
rbn_spots = rbn_spots.assign(db=rbn_spots_located.db).assign(dx_lat=rbn_spots_located.dx_lat).assign(dx_lon=rbn_spots_located.dx_lon)
rbn_spots = rbn_spots.loc[rbn_spots.db.notnull()].loc[rbn_spots.dx_lat.notnull()].loc[rbn_spots.dx_lon.notnull()]

rbn_grps = rbn_spots.groupby('callsign')

k2mff2 = rbn_grps.get_group('K2MFF-2')
k2mff3 = rbn_grps.get_group('K2MFF-3')

not_k2mff2 = rbn_spots[rbn_spots.callsign != 'K2MFF-2']
not_k2mff3 = rbn_spots[rbn_spots.callsign != 'K2MFF-3']

k2mff2 = k2mff2.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
k2mff2 = k2mff2.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

k2mff3 = k2mff3.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
k2mff3 = k2mff3.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

not_k2mff2 = not_k2mff2.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
not_k2mff2 = not_k2mff2.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

not_k2mff3 = not_k2mff2.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
not_k2mff3 = not_k2mff2.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

import matplotlib
import matplotlib.pyplot as plt

f = plt.figure(figsize=(10, 10), dpi=500)

ax_k2mff2 = f.add_subplot(221, projection='polar')
ax_k2mff3 = f.add_subplot(222, projection='polar')
ax_not_k2mff2 = f.add_subplot(223, projection='polar')
ax_not_k2mff3 = f.add_subplot(224, projection='polar')

norm = matplotlib.colors.Normalize(vmin=0, vmax=50)

ax_k2mff2.scatter(k2mff2.azimuth, k2mff2.distance, c=k2mff2.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'), s=10)
ax_k2mff2.set_title('K2MFF-2')
ax_k2mff2.set_theta_offset(np.pi / 2)
ax_k2mff2.set_ylim(0, 10000)

ax_not_k2mff2.scatter(not_k2mff2.azimuth, not_k2mff2.distance, c='#696969', marker='x', alpha=0.1, s=2)
ax_not_k2mff2.scatter(k2mff2.azimuth, k2mff2.distance, c=k2mff2.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'), s=10)
ax_not_k2mff2.set_theta_offset(np.pi / 2)
ax_not_k2mff2.set_ylim(0, 10000)

ax_k2mff3.scatter(k2mff3.azimuth, k2mff3.distance, c=k2mff3.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'), s=10)
ax_k2mff3.set_title('K2MFF-3')
ax_k2mff3.set_theta_offset(np.pi / 2)
ax_k2mff3.set_ylim(0, 10000)

ax_not_k2mff3.scatter(not_k2mff3.azimuth, not_k2mff3.distance, c='#696969', marker='x', alpha=0.1, s=2)
ax_not_k2mff3.scatter(k2mff3.azimuth, k2mff3.distance, c=k2mff3.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'), s=10)
ax_not_k2mff3.set_theta_offset(np.pi / 2)
ax_not_k2mff3.set_ylim(0, 10000)

f.suptitle('Comparison between K2MFF-2 and K2MFF-3 for 2017-07-23')
f.savefig('k2mff2_vs_km2ff3')
