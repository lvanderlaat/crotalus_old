

def get_instrument_scale(inventory, station, channel, time):
    """Get instrument scale

    Instead of computing the complete deconvolution, just divide the trace by
    the scale to remove instrument response

    Parameters
    ----------
    inventory : obspy.inventory
        Inventory containing instrument response
    station : str
        Station code
    channel : str
        Channel code
    time : obspy.UTCDateTime
        Time where the instrument is active

    Returns
    -------
    value : float
        Instrument response sensitivity scale
    input_units : str
        Instrument

    """
    channel = inventory.select(station=station, channel=channel, time=time)[0][0][0]
    instrument_sensitivity = channel.response.instrument_sensitivity
    value = instrument_sensitivity.value
    input_units = instrument_sensitivity.input_units
    return value, input_units
