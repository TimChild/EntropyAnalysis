import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import os

import dat_analysis
from dat_analysis import useful_functions as U

default_config = dict(
    toImageButtonOptions={'format': 'png',  # one of png, svg, jpeg, webp
                      'scale': 2  # Multiply title/legend/axis/canvas sizes by this factor
})

default_layout = dict(template="plotly_white",
            xaxis=dict(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
            ),
            yaxis=dict(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
            ))

fig_dir = 'figures/'
os.makedirs(fig_dir, exist_ok=True)


def default_fig(rows=1, cols=1):
    if rows != 1 or cols != 1:
        fig = make_subplots(rows=rows, cols=cols)
    else:
        fig = go.Figure()
    fig.update_layout(**default_layout)
    return fig

def get_dat(datnum):
    return dat_analysis.get_dat(datnum, host='qdev-xld', user='Tim', experiment='202208_KondoConductanceDots')

print('importing')