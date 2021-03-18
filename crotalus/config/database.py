# Python Standard Library
from collections import namedtuple
from datetime import datetime

# Other dependencies
import pandas as pd

# Local files


def get_configuration(measurement, conn):
    """ Get configuration for measurement

    Options for measurement are:
        * RSEM
        * SSAM
        * DSAR

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
        f"""SELECT * FROM configuration
        WHERE measurement='{measurement}';""",
        conn)
    c = df.iloc[0].settings
    return namedtuple('c', c.keys())(**c)
