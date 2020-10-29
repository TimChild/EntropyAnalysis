from JupyterImport import *
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
root_logger.setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def combine_graphs(figs):
    fig = make_subplots(1, len(figs), subplot_titles = [f.layout.title.text for f in figs])

    for i, f in enumerate(figs):
        for d in f.data:
            fig.add_trace(d,row=1, col=i+1)
            if isinstance(fig.data[-1], go.Heatmap):
                fig.data[-1].update(coloraxis='coloraxis')
    
    return fig


allowed_datnums = range(4000, 10000)
max_points_per_row = 1000

def avg_ct(datnum):
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.Data.x_array
        y = dat.Transition.avg_data

        x_label = dat.Logs.x_label
        y_label = "Current /nA"

        x, y = CU.bin_data([x, y], bin_size = np.ceil(y.shape[-1]/max_points_per_row))

        fig = go.Figure()
        fig.add_trace(go.Scatter(mode = 'markers', x=x, y=y))
        fig.update_layout(xaxis_title = x_label, 
                          yaxis_title = y_label,
                         title = f'Dat{dat.datnum}')
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()

def avg_entropy(datnum):
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.SquareEntropy.Processed.outputs.x
        y = dat.SquareEntropy.Processed.outputs.entropy_signal

        x_label = dat.Logs.x_label
        y_label = "Current /nA"

        max_points_per_row = 1000

        x, y = CU.bin_data([x, y], bin_size = np.ceil(y.shape[-1]/max_points_per_row))

        fig = go.Figure()
        fig.add_trace(go.Scatter(mode = 'markers', x=x, y=y))
        fig.update_layout(xaxis_title = x_label, 
                      yaxis_title = y_label,
                     title = f'Dat{dat.datnum}')
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()
    
def all_ct(datnum):
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.Data.x_array
        z = dat.Data.Exp_cscurrent_2d
        y = list(range(z.shape[0]))

        x_label = dat.Logs.x_label
        y_label = dat.Logs.y_label
        z_label = "Current /nA"

        max_points_per_row = 1000

        x, z = CU.bin_data([x, z], bin_size = np.ceil(z.shape[-1]/max_points_per_row))
        fig = go.Figure()
        fig.add_trace(go.Heatmap(x=x, y=y, z=z))
        fig.update_layout(xaxis_title = x_label, 
                          yaxis_title = y_label,
                         coloraxis = dict(colorbar=dict(title=z_label)),
                         title = f'Dat{dat.datnum}')
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()
    
def all_entropy(datnum):
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.SquareEntropy.Processed.outputs.x
        z = dat.SquareEntropy.entropy_data
        y = list(range(z.shape[0]))

        x_label = dat.Logs.x_label
        y_label = dat.Logs.y_label
        z_label = "Current /nA"

        max_points_per_row = 1000

        x, z = CU.bin_data([x, z], bin_size = np.ceil(z.shape[-1]/max_points_per_row))
        fig = go.Figure()
        fig.add_trace(go.Heatmap(x=x, y=y, z=z))
        fig.update_layout(xaxis_title = x_label, 
                          yaxis_title = y_label,
                         coloraxis = dict(colorbar=dict(title=z_label)),
                         title = f'Dat{dat.datnum}')
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()
    
def transition_values(datnum):
    from src.DatObject.Attributes import Transition as T
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.Data.x_array
        z = dat.Data.Exp_cscurrent_2d
        y = np.array(range(z.shape[0]))

        x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))

        pars = T.get_param_estimates(x, z)
        fits = T.transition_fits(x, z, func=T.i_sense, params=pars, auto_bin=True)

        fig = go.Figure()
        for k in fits[0].best_values.keys():
            fvals = [f.best_values.get(k, None) for f in fits]
            fig.add_trace(go.Scatter(mode='markers', x = fvals, y = y, name=f'{k} values'))

        fig.update_layout(xaxis_title='Fit values', yaxis_title='Y array', title=f'CT fit values for Dat{dat.datnum}')
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()
    
    
def entropy_values(datnum):
    from src.DatObject.Attributes import Entropy as E
    datnum = int(datnum)
    if datnum in allowed_datnums:
        dat = get_dat(datnum)
        x = dat.SquareEntropy.Processed.outputs.x
        z = dat.SquareEntropy.entropy_data
        y = np.array(range(z.shape[0]))

        x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))

        pars = E.get_param_estimates(x, z)
        fits = E.entropy_fits(x, z, params=pars, auto_bin=True)

        fig = go.Figure()
        for k in fits[0].best_values.keys():
            y = y  # From above
            fvals = [f.best_values.get(k, None) for f in fits]
            fig.add_trace(go.Scatter(mode='markers', x = fvals, y = y, name=f'{k} values'))

        fig.update_layout(xaxis_title='Fit values', yaxis_title='Y array', title=f'Entropy fit values for Dat{dat.datnum}')
    
        return fig
    else:
        logger.warning(f'{datnum} not in allowed datnums')
        return go.Figure()

    
    
all_graphs = dict(avg_ct = avg_ct, avg_entropy=avg_entropy, all_ct = all_ct, all_entropy=all_entropy, transition_values=transition_values, entropy_values=entropy_values)


# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Dat Avg Data"),
    dcc.Graph(id='graph'),
    
    html.Label([
        "Choose Dat:  ",
        dcc.Input(
        id="datnum-input", value=8337)
    ]),
    html.Label(["Choose Graph Type", dcc.Dropdown(
        id="graph-type", value="avg_ct", options=[{'label': k, 'value': k} for k in all_graphs], multi=True)
               ]),
])
# Define callback to update graph
# app.callback(
#     Output('graph', 'figure'),
#     [Input("datnum-dropdown", "value")]
# )(display_dat)

@app.callback(
    Output('graph', 'figure'),
    [Input("datnum-input", "value"),
    Input("graph-type", "value")]
)
def graph_chooser(datnum, graph_types):
    graph_types = CU.ensure_list(graph_types)
    figs = list()
    for k in graph_types:
        if k in all_graphs:
            figs.append(all_graphs[k](datnum))
        else:
            figs.append(go.Figure())
    
    fig = combine_graphs(figs)
    return fig
    


# Run app and display result inline in the notebook
app.run_server(mode='jupyterlab')
