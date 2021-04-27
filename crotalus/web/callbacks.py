# Python Standard Library

# Other dependencies
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Local files
from crotalus.web.apps import app
from crotalus.web.queries import (
    get_stations_options, get_channel_options, query, get_client, get_network
)
from crotalus.web.plots import plot


@app.callback(
    Output('station-dropdown', 'options'),
    Input('volcano-dropdown', 'value'))
def set_stations_options(selected_volcano):
    return get_stations_options(selected_volcano)


@app.callback(
    Output('station-dropdown', 'value'),
    Input('station-dropdown', 'options'))
def set_stations_value(available_options):
    # return available_options[0]['value']
    return 2


@app.callback(
    Output('channel-dropdown', 'options'),
    Input('station-dropdown', 'value'))
def set_channel_options(selected_station):
    return get_channel_options(selected_station)


@app.callback(
    Output('channel-dropdown', 'value'),
    Input('channel-dropdown', 'options'))
def set_channel_value(available_options):
    # return available_options[0]['value']
    return 7


@app.callback(
    Output('loading', 'children'),
    Output('graph', 'figure'),

    [Input('submit-button', 'n_clicks')],

    state=[
        State('channel-dropdown', 'value'),
        State('measurement-checklist', 'value'),
        State('datetime-picker', 'startDate'),
        State('datetime-picker', 'endDate')
    ]
)
def update_output_div(n_clicks, channel_id, measurements, startDate, endDate):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = query(channel_id, measurements, startDate, endDate)
        return None, plot(measurements, df)

