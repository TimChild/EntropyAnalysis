import abc
import h5py
from dataclasses import dataclass
import numpy as np
import os
import sys
import logging
from typing import List, Tuple, Union, Optional
logger = logging.getLogger(__name__)
sys.path.insert(1, r'D:\OneDrive\UBC LAB\GitHub\Python\PyDatAnalysis')
import src.HDF_Util as HDU
import src.CoreUtil as CU


## Possible fix for an overlapping 'efit_info' empty attr in EA_values group which prevents the true 'efit_info' from loading

for dat in dats:
    g = dat.Other.group
    if (vg := g.get('EA_values', None)) is not None:
        if 'efit_info' in vg.attrs.keys():
            del vg.attrs['efit_info']
            print(f'deleted efit_info in dat{dat.datnum}')
            g.file.flush()


d = [
    dict(name='LCSS', func=lambda dat: dat.Logs.fds['LCSS'], precision='.2f', units='mV', position=0),
    dict(name='LCB',  func=lambda dat: dat.Logs.fds['LCB'], precision='.2f', units='mV', position=1),
]








