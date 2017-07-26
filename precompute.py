#!/usr/bin/env python3

import numpy as np
import pandas as pd

from pyporktools.qrz import QRZSession

qrz = QRZSession('w2naf', 'hamscience')

def get_latlon(x):
    global qrz
    
    try:
        call = qrz.lookup_callsign(x['dx'])
        x['dx_lat'] = call['lat']
        x['dx_lon'] = call['lon']
    except:
        x['dx_lat'] = None
        x['dx_lon'] = None
    
    return x

rbn_spots = pd.read_csv('20170723.csv', header=0, usecols=['dx', 'db'])

print('Getting dx lat & lon.')

rbn_spots = rbn_spots.apply(get_latlon, axis=1)

print('Removing empty values.')

rbn_spots = rbn_spots.loc[rbn_spots.dx_lat.notnull()].loc[rbn_spots.dx_lon.notnull()]

print('Saving.')

rbn_spots.to_csv('20170723_located.csv')
