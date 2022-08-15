from dataclasses import dataclass
from typing import Optional, Tuple, Union, TYPE_CHECKING, List, Dict, Any
import re
import logging

import lmfit as lm
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dat_analysis.analysis_tools.new_procedures import Process, DataPlotter, PlottableData
from dat_analysis.analysis_tools.general_fitting import calculate_fit, FitInfo
from dat_analysis.dat.dat_hdf import get_dat
import dat_analysis.useful_functions as U

if TYPE_CHECKING:
    import h5py

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    import plotly.io as pio
    pio.renderers.default = 'browser'
    # datnums = [156, 157, 158, 159]
    datnums = [156] #, 157, 158, 159]

    for num in datnums:
        dat = get_dat(num)
        data = dat.Data.get_data('wave0_2d')
        x = dat.Data.x

        fig = go.Figure()
        for i, d in enumerate(data):
            d = U.decimate(d, dat.Logs.measure_freq, numpnts=300)
            x = U.get_matching_x(x, d)
            fig.add_trace(go.Scatter(x=x, y=d, mode='lines', name=f'row{i}'))

        fig.show()
        dat.Logs.get('')