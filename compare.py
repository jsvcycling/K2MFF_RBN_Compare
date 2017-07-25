#!/usr/bin/env python3

import numpy as np
import pandas as pd

K2MFF_LAT = 40.9080035
K2MFF_LON = -74.9245285

# This is really inefficient
def get_azm(qrz, callsign):
    try:
        call = qrz.lookup_callsign(callsign)
        return geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON,
                                      call['lat'], call['lon']) + 180.
    except:
        return None

# This is really inefficient
def get_dist(qrz, callsign):
    try:
        call = qrz.lookup_callsign(callsign)
        return geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON,
                                       call['lat'], call['lon']) * 6378.14
    except:
        return None

from hamsci import geopack
from pyporktools.qrz import QRZSession

rbn_spots = pd.read_csv('20170723.csv', header=0, usecols=['callsign', 'dx', 'db'])

rbn_grps = rbn_spots.groupby('callsign')

k2mff2_grp = rbn_grps.get_group('K2MFF-2')
k2mff3_grp = rbn_grps.get_group('K2MFF-3')

qrz = QRZSession('w2naf', 'hamscience')

k2mff2_grp.loc[:, 'azimuth'] = k2mff2_grp.loc[:, 'dx'].apply(lambda x: get_azm(qrz, x))
k2mff3_grp.loc[:, 'azimuth'] = k2mff3_grp.loc[:, 'dx'].apply(lambda x: get_azm(qrz, x))

k2mff2_grp.loc[:, 'distance'] = k2mff2_grp.loc[:, 'dx'].apply(lambda x: get_dist(qrz, x))
k2mff3_grp.loc[:, 'distance'] = k2mff3_grp.loc[:, 'dx'].apply(lambda x: get_dist(qrz, x))

k2mff2_grp = k2mff2_grp.loc[k2mff2_grp.azimuth.notnull()].loc[k2mff2_grp.distance.notnull()]
k2mff3_grp = k2mff3_grp.loc[k2mff3_grp.azimuth.notnull()].loc[k2mff3_grp.distance.notnull()]

import matplotlib
import matplotlib.pyplot as plt

f = plt.figure(figsize=(10, 10), dpi=300)

ax_tl = f.add_subplot(221, projection='polar')
ax_tr = f.add_subplot(222, projection='polar')
ax_bl = f.add_subplot(223, projection='polar')
ax_br = f.add_subplot(224, projection='polar')

norm = matplotlib.colors.Normalize(vmin=0, vmax=50)

ax_tl.scatter(k2mff2_grp.azimuth, k2mff2_grp.distance, c=k2mff2_grp.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'))
ax_tl.set_title('K2MFF-2')
ax_tl.set_theta_offset(np.pi / 2)
ax_tl.set_ylim(0, 4000)

ax_tr.scatter(k2mff3_grp.azimuth, k2mff3_grp.distance, c=k2mff3_grp.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'))
ax_tr.set_title('K2MFF-3')
ax_tr.set_theta_offset(np.pi / 2)
ax_tr.set_ylim(0, 4000)

ax_bl.scatter(k2mff2_grp.azimuth, k2mff2_grp.distance, c=k2mff2_grp.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'))
ax_bl.set_theta_offset(np.pi / 2)
ax_bl.set_ylim(0, 10000)

ax_br.scatter(k2mff3_grp.azimuth, k2mff3_grp.distance, c=k2mff3_grp.db, alpha=0.5, norm=norm, cmap=plt.get_cmap('jet'))
ax_br.set_theta_offset(np.pi / 2)
ax_br.set_ylim(0, 10000)

f.suptitle('Comparison between K2MFF-2 and K2MFF-3 for 2017-07-23')
f.savefig('k2mff-2_vs_k2mff-3')
