# Add PyDatAnalysis to path
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, r'D:\OneDrive\UBC LAB\GitHub\Python\PyDatAnalysis')

export_path = 'Exports/'

# Import my commonly used packages
from src import CoreUtil as CU
from src.DatObject.Make_Dat import DatHandler
from src.DatObject.DatHDF import DatHDF
from src.Characters import *
from src.DataStandardize.Standardize_Util import wait_for  # Sets a thread waiting for a dat to finish
from src.Plotting.Mpl import Plots as P, PlotUtil as PU
from src.Plotting.Plotly import PlotlyUtil as PlU

#  Common packages I use
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import inspect          # Useful for inspect.getSource()  # for storing code in HDF
import lmfit as lm
from typing import List, Tuple, Union, Set, NamedTuple, Dict, Optional  # Good for asserting types
import logging
from progressbar import progressbar

#  The Experiment's I'm currently working with. Makes it easier to get to Config/ESI/Fixes
import src.DataStandardize.ExpSpecific.Sep20 as Sep20
import src.DataStandardize.ExpSpecific.Aug20 as Aug20
import src.DataStandardize.ExpSpecific.Jun20 as Jun20
import src.DataStandardize.ExpSpecific.Jan20 as Jan20

# Most commonly used functions and classes
get_dat = DatHandler.get_dat
get_dats = DatHandler.get_dats
SepESI = Sep20.SepESI
AugESI = Aug20.AugESI
JunESI = Jun20.JunESI
JanESI = Jan20.JanESI

root_logger = logging.getLogger()
if not root_logger.handlers:
    CU.set_default_logging()