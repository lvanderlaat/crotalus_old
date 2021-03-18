# Python Standard Library

# Other dependencies
import pandas as pd

# Local files
from crotalus.config.database import get_configuration
from crotalus.dsp.spectrum import get_8ve_bands


def get_volcanoes_options():
    df = pd.read_sql_query('SELECT * FROM volcano;', conn)
    return [dict(label=row['name'], value=row.id) for i, row in df.iterrows()]


def get_stations_options(volcano_id):
    df = pd.read_sql_query(
        f'SELECT * FROM station WHERE volcano_id = {volcano_id};', conn
    )
    return [dict(label=row.station, value=row.id) for i, row in df.iterrows()]


def get_channel_options(station_id):
    df = pd.read_sql_query(
        f'SELECT * FROM channel WHERE station_id = {station_id}; ', conn
    )
    return [dict(label=row.channel, value=row.id) for i, row in df.iterrows()]


def get_measurments_options():
    df = pd.read_sql_query(
        """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = N'continuous'
        """,
        conn
    )
    return [
        dict(label=row.column_name, value=row.column_name)
        for i, row in df.iterrows()
        if row.column_name not in ['channel_id', 'time']
    ]


def query(channel_id, measurements, starttime, endtime):
    measurements_str = ', '.join(measurements)
    df = pd.read_sql_query(
        f"""
        SELECT time, {measurements_str} FROM continuous
        WHERE (channel_id = '{channel_id}') AND
        (time BETWEEN timestamp '{starttime}' and timestamp '{endtime}');
        """,
        conn
    )
    df.index = pd.to_datetime(df.time, unit='s')
    df.sort_index(inplace=True)
    return df


def get_ssam_freq():
    SAMPLING_RATE = 100.
    c = get_configuration('ssam', conn)
    fl, fc, fu = get_8ve_bands(SAMPLING_RATE/c.decimation_factor, c.fraction,
                               c.f_lower, c.f_upper)
    return fl
