# Python Standard Library

# Other dependencies
import dash_core_components as dcc
import dash_html_components as html
from dash_datetimepicker import DashDatetimepicker

# Local files
from crotalus.web.app import app
from crotalus.web.queries import get_volcanoes_options, get_measurments_options


layout = html.Div(
    id='output',
    children=[
        html.Label('Volcano'),

        dcc.Dropdown(
            id='volcano-dropdown',
            options=get_volcanoes_options(),
            value=get_volcanoes_options()[0]['value']
        ),

        html.Label('Station'),

        dcc.Dropdown(id='station-dropdown'),

        html.Label('Channel'),

        dcc.Dropdown(id='channel-dropdown'),

        html.Label('Measurements'),

        dcc.Checklist(
            id='measurement-checklist',
            options=get_measurments_options()
        ),

        html.Label('Time range'),

        DashDatetimepicker(
            id='datetime-picker',
            # TODO use today
            startDate='2021-01-01T20:00:00.000Z',
            endDate='2021-01-01T20:10:00.000Z'
        ),

        html.Button('Submit', id='submit-button'),

        dcc.Loading(
            id="loading",
            fullscreen=True,
        ),

        dcc.Graph(id='graph')
        # html.Div(id='print')
    ]
)
