# Python Standard Library

# Other dependencies
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Local files
from crotalus.web.queries import get_ssam_freq


fl = get_ssam_freq()


def plot(measurements, df):
    fig = make_subplots(rows=len(measurements), cols=1, shared_xaxes=True,)
    for row, m in enumerate(measurements, start=1):
        trace = go.Scatter(x=df.index, y=df[m], mode='lines', name=m)
        if m == 'ssam':
            Sxx = np.array(df.ssam.tolist()).T # Hacer la matriz
            trace = go.Heatmap(x=df.index, y=fl, z=np.log(Sxx))
            fig.update_yaxes(type="log", row=row, col=1)
        fig.add_trace(trace, row=row, col=1)

        fig.update_layout(height=len(measurements)*300)
    return fig
