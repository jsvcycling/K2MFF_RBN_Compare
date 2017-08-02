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

for band in BAND_LIST:
    f, ax = plt.subplots(1, 2, figsize=(16, 9), subplot_kw=dict(projection='polar'))

    not_k2mff2 = rbn_spots[(rbn_spots.band == band) & (rbn_spots.callsign != 'K2MFF-2')]
    not_k2mff2 = not_k2mff2.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
    not_k2mff2 = not_k2mff2.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)
    
    not_k2mff3 = rbn_spots[(rbn_spots.band == band) & (rbn_spots.callsign != 'K2MFF-3')]
    not_k2mff3 = not_k2mff3.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
    not_k2mff3 = not_k2mff3.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

    ax[0].scatter(not_k2mff2.azimuth, not_k2mff2.distance, c='#696969', marker='x', alpha=0.2, s=2)
    ax[1].scatter(not_k2mff3.azimuth, not_k2mff3.distance, c='#696969', marker='x', alpha=0.2, s=2)
    
    try:
        df = groups.get_group((band, 'K2MFF-2'))

        df = df.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
        df = df.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

        ax[0].scatter(df.azimuth, df.distance, c=df.db, alpha=0.5, norm=norm, cmap=cmap, s=30)
    except KeyError as e:
        print('Key Error: {}'.format(e))

    try:
        df = groups.get_group((band, 'K2MFF-3'))
        
        df = df.assign(azimuth=lambda x: geopack.greatCircleAzm(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']))
        df = df.assign(distance=lambda x: geopack.greatCircleDist(K2MFF_LAT, K2MFF_LON, x['dx_lat'], x['dx_lon']) * 6378.137)

        ax[1].scatter(df.azimuth, df.distance, c=df.db, alpha=0.5, norm=norm, cmap=cmap, s=30)
    except KeyError as e:
        print('Key Error: {}'.format(e))

    
    ax[0].set_theta_direction(-1)
    ax[0].set_theta_offset(np.pi / 2)
    ax[0].set_ylim(0, 10000)
    
    ax[1].set_theta_direction(-1)
    ax[1].set_theta_offset(np.pi / 2)
    ax[1].set_ylim(0, 10000)

    f.savefig('render_{}'.format(band), bbox_inches='tight')
    plt.close(f)
