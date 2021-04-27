# Python Standard Library
from collections import namedtuple
from datetime import datetime

# Other dependencies
import pandas as pd

# Local files


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
