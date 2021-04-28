# Python Standard Library
from collections import namedtuple
from datetime import datetime

# Other dependencies
import pandas as pd

# Local files


def query_general_conf(conn):
    df = pd.read_sql_query("""SELECT * FROM settings LIMIT 1;""", conn)
    c = df.iloc[0].to_dict()
    return namedtuple('c', c.keys())(**c)


def continuous_extraction_channels(conn):
    """ Get channels for continuous extraction

    Queries the database to obtain the stations to process in continuous

    Parameters
    ----------
    conn : SQL connection
        SQL connection

    Returns
    -------
    df : pandas.DataFrame
        filtered 'channel' table from the database

    """
    df = pd.read_sql_query(
        'SELECT * FROM channel WHERE continuous_extraction',
        conn
    )
    return df


def get_configuration(feature, conn):
    """ Get configuration for feature

    Parameters
    ----------
    measurement : str
        Measurement
    conn : SQL connection
        SQL connection

    Returns
    -------
    c : namedtuple
        Configuration settings
    """
    df = pd.read_sql_query(
        f"""SELECT * FROM feature
        WHERE feature_name='{feature}';""",
        conn)
    c = df.iloc[0].settings
    return namedtuple('c', c.keys())(**c)


def query_feature_conf(conn):
    """ Get configuration for all features

    Parameters
    ----------
    conn : SQL connection
        SQL connection

    Returns
    -------
    c : namedtuple
        Configuration settings
    """
    df = pd.read_sql_query(
        f"""SELECT feature_name, settings FROM feature;""",
        conn)
    c = dict()
    for i, row in df.iterrows():
        c[row.feature_name] = namedtuple(
            row.feature_name,
            row.settings.keys()
        )(**row.settings)
    return namedtuple('c', c.keys())(**c)
