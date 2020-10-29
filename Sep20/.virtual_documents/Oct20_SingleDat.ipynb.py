from JupyterImport import *
root_logger.setLevel(logging.WARNING)


# dats = get_dats(list(range(7848, 7855)))
# dats = get_dats((8885, 8885+1))
dats = [get_dat(8799)]


for dat in dats:
    print(dat.datnum, dat.Logs.comments)





figs = list()
for dat in dats[:1]:
    x = dat.Data.x_array
    y = dat.Transition.avg_data
    
    x_label = dat.Logs.x_label
    y_label = "Current /nA"

    max_points_per_row = 1000

    x, y = CU.bin_data([x, y], bin_size = np.ceil(y.shape[-1]/max_points_per_row))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode = 'markers', x=x, y=y))
    fig.update_layout(xaxis_title = x_label, 
                      yaxis_title = y_label,
                     title = f'Dat{dat.datnum}')
    figs.append(fig)

for fig in figs:
    fig.show()    


figs = list()
for dat in dats[:1]:
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
    figs.append(fig)

for fig in figs:
    fig.show()    


figs = list()
for dat in dats:
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
    figs.append(fig)

for fig in figs:
    fig.show()


fig = make_subplots(1, len(figs), subplot_titles = [f.layout.title.text for f in figs])

for i, f in enumerate(figs):
    fig.add_trace(f.data[0],row=1, col=i+1)
    fig.data[-1].update(coloraxis='coloraxis')
fig


figs = list()
for dat in dats:
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
    figs.append(fig)

for fig in figs:
    fig.show()


fig = make_subplots(1, len(figs), subplot_titles = [f.layout.title.text for f in figs])

for i, f in enumerate(figs):
    fig.add_trace(f.data[0],row=1, col=i+1)
    fig.data[-1].update(coloraxis='coloraxis')
fig


from src.DatObject.Attributes import Transition as T, Entropy as E, SquareEntropy as SE

figs, all_ct_fits = list(), list()
for dat in dats:

    x = dat.Data.x_array
    z = dat.Data.Exp_cscurrent_2d
    y = np.array(range(z.shape[0]))

    x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))

    pars = T.get_param_estimates(x, z)
    fits = T.transition_fits(x, z, func=T.i_sense, params=pars, auto_bin=True)
    all_ct_fits.append(fits)
    
    fig = go.Figure()
    for k in fits[0].best_values.keys():
        fvals = [f.best_values.get(k, None) for f in fits]
        fig.add_trace(go.Scatter(mode='markers', x = fvals, y = y, name=f'{k} values'))

    fig.update_layout(xaxis_title='Fit values', yaxis_title='Y array', title=f'CT fit values for Dat{dat.datnum}')
    figs.append(fig)

for fig in figs:
    fig.show()


for fig in figs:
    fig.write_html(f'Exports/{fig.layout.title.text}.html')


figs, all_entropy_fits = list(), list()
for dat in dats:
    x = dat.SquareEntropy.Processed.outputs.x
    y = np.array(range(z.shape[0]))
    z = dat.SquareEntropy.entropy_data

    x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))

    pars = E.get_param_estimates(x, z)
    fits = E.entropy_fits(x, z, params=pars, auto_bin=True)
    all_entropy_fits.append(fits)

    fig = go.Figure()
    for k in fits[0].best_values.keys():
        y = y  # From above
        fvals = [f.best_values.get(k, None) for f in fits]
        fig.add_trace(go.Scatter(mode='markers', x = fvals, y = y, name=f'{k} values'))

    fig.update_layout(xaxis_title='Fit values', yaxis_title='Y array', title=f'Entropy fit values for Dat{dat.datnum}')
    figs.append(fig)
    
for fig in figs:
    fig.show()


for fig in figs:
    fig.write_html(f'Exports/{fig.layout.title.text}.html')


if len(dats) == 1:
    datnum = dats[0].datnum
else:
    datnum = 8885
rows = [0]

all_fits = all_ct_fits
# all_fits = all_entropy_fits

dd = {dat.datnum: (dat, fits) for dat, fits in zip(dats, all_fits)}
dat, fits = dd[datnum]

x = dat.Data.x_array
z = dat.Data.Exp_cscurrent_2d

# x = dat.SquareEntropy.Processed.outputs.x
# z = dat.SquareEntropy.entropy_data

# x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))
x = x[::50]
z = z[:, ::50]

row_data = z[rows,]
fits_to_show = np.array(fits)[rows,]  

fig = go.Figure()
for i, (r, rnum) in enumerate(zip(row_data, rows)):
    name = f'Row {rnum}'
    fig.add_trace(go.Scatter(mode='markers+lines', x=x, y=r, name=name, legendgroup=name))
    if fits_to_show is not None:
        f = fits_to_show[i]
        fig.add_trace(go.Scatter(mode='lines', x=x, y=f.eval(x=x), legendgroup=name, name=name+'_fit'))
        print(f.best_values)
fig.update_layout(title=f'Dat{dat.datnum}: Rows {rows} of Transition Data')
fig.show()


# datnum = 7852
# rows = [4]

all_fits = all_entropy_fits

dd = {dat.datnum: (dat, fits) for dat, fits in zip(dats, all_fits)}
dat, fits = dd[datnum]

x = dat.SquareEntropy.Processed.outputs.x
z = dat.SquareEntropy.entropy_data

x, z = CU.bin_data([x, z], bin_size=np.ceil(z.shape[-1]/max_points_per_row))

row_data = z[rows,]
fits_to_show = np.array(fits)[rows,]  

fig = go.Figure()
for i, (r, rnum) in enumerate(zip(row_data, rows)):
    name = f'Row {rnum}'
    fig.add_trace(go.Scatter(mode='markers+lines', x=x, y=r, name=name, legendgroup=name))
    if fits_to_show is not None:
        f = fits_to_show[i]
        fig.add_trace(go.Scatter(mode='lines', x=x, y=f.eval(x=x), legendgroup=name, name=name+'_fit'))
        print(f.best_values)
fig.show()



for dat in dats:
    print(dat.datnum, dat.Logs.fds, dat.Logs.comments)


params = {'Two Part': lambda dat: dat.Logs.part_of[1] == 2,
          'Part': lambda dat: dat.Logs.part_of[0],
          'Time elapsed': lambda dat: dat.Logs.time_elapsed,
          'Width': lambda dat: dat.Data.x_array[-1]-dat.Data.x_array[0], 
          'Repeats': lambda dat: dat.Data.y_array.shape[-1],
         'LCSS': lambda dat: dat.Logs.fds['LCSS'],
         'LCSQ': lambda dat: dat.Logs.fds['LCSQ'],
         'LP*2': lambda dat: dat.Logs.fds['LP*2'],
         'LCT': lambda dat: dat.Logs.fds.get('LCT', None),
         'LCT/0.196': lambda dat: dat.Logs.fds.get('LCT/0.196', None),
         'LCB': lambda dat: dat.Logs.fds['LCB'],
         'dS': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_values.dS', None),
          'dS uncertainty': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_uncertainties.fit_dS', None),
          'Uncertainty batch size': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_analysis_params.batch_uncertainty', None),
          'Entropy fit range': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_analysis_params.E_fit_range', None),
          'Transition amp': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_values.amp', None),
          'Amp uncertainty': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_uncertainties.amp', None),
          'Theta': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_values.tc', None),
          'Theta uncertainty': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_uncertainties.tc', None),
          'Transition fit range': lambda dat: CU.get_nested_attr_default(dat, 'Other.EA_analysis_params.CT_fit_range', None),
          'RCSS': lambda dat: dat.Logs.bds['RCSS'],
          'RCSQ': lambda dat: dat.Logs.bds['RCSQ'],
          'RCT': lambda dat: dat.Logs.bds['RCT'],
          'RCB': lambda dat: dat.Logs.bds['RCB'],
          'R2T(10M)': lambda dat: dat.Logs.fds.get('R2T(10M)', None),
          'R2T/0.001': lambda dat: dat.Logs.fds.get('R2T/0.001', None),
          'HQPC bias mV': lambda dat: dat.SquareEntropy.SquareAWG.AWs[0][0][1]
         }

df = pd.DataFrame()
for dat in dats:
    data = pd.Series({k: v(dat) for k, v in params.items()}, name=f'Dat{dat.datnum}')
    df = pd.concat((df, data), axis=1)

    
df



