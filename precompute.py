#!/usr/bin/env python3

import os

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

for filename in os.listdir('./raw'):
    print('Operating on: ./raw/{}'.format(filename))
    df = pd.read_csv('./raw/{}'.format(filename), header=0)
    df = df.apply(get_latlon, axis=1)
    df = df[df.dx_lat.notnull() & df.dx_lon.notnull()]
    df.to_csv('./located/{}'.format(filename, index=False))
