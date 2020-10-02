



fig = go.Figure()

ds = p1_dats
x_range = [-4000, -3800]

state = ['Normal', 'Channel Closed', 'Heater Closed']
per_state = ['Weak', 'Strong']
labels = [', '.join([b, a]) for a, b in product(state, per_state)]

for dat, label in zip(ds, labels):
    x = dat.Data.x_array
    indexs = CU.get_data_index(x, x_range)
    z = dat.Data.Exp_channel_2d[0][indexs[0]:indexs[1]]
    x = x[indexs[0]:indexs[1]]
    fig.add_trace(go.Scatter(x=x, y=z, name=f'{dat.datnum}, {label}'))

PlU.fig_setup(fig, title='Channel Current with no correction bias', x_label='LP*200 /mV', y_label='Current /nA', legend_title='Datnum, Coupling, HQPC state')
fig
fig.write_html(export_path+f'Dats{ds[0].datnum}-{ds[-1].datnum} -- Channel Current with no correction bias - {x[0]:.0f}mV - {x[-1]:.0f}mV.html')








fig = go.Figure()

ds = p1_dats
x_range = (-4000, -3800)

state = ['Normal', 'Channel Closed', 'Heater Closed']
per_state = ['Weak', 'Strong']
labels = [', '.join([b, a]) for a, b in product(state, per_state)]

for dat, label in zip(ds, labels):
    wavelen = dat.Logs.AWG.wave_len
    freq = dat.Logs.AWG.measureFreq/wavelen
    
    x = dat.Data.x_array
    indexs = CU.get_data_index(x, x_range)
    z = dat.Data.Exp_channel_2d[0][indexs[0]:indexs[1]]
    x = x[indexs[0]:indexs[1]]
    z = np.mean(dat.Data.Exp_cscurrent_2d[indexs[0]:indexs[1]-(indexs[1]-indexs[0])%wavelen], axis=0)
    z = np.reshape(z, (-1, wavelen))
    z = np.mean(z, axis=0)
    z = z-np.mean(z)
    lin_x = np.linspace(0, 1, wavelen)
    fig.add_trace(go.Scatter(x=lin_x, y=z, name=f'{dat.datnum}, {label}'))

PlU.fig_setup(fig, title=f'Single wave averaged over all rows from {x:.0f}mV to {x[-1]:.0f}mV - wavelen={wavelen}samples, freq={freq:.1f}Hz', x_label='Fraction of single cycle', y_label='Delta Current /nA', legend_title='Datnum, Coupling, HQPC state')
fig.update_yaxes(showspikes=True)
fig

fig.write_html(export_path+f'Dats{ds[0].datnum}-{ds[-1].datnum} -- Averaged single cycle from {x[0]:.0f}mV to {x[-1]:.0f}mV.html')