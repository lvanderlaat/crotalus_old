# Python Standard Library

# Other dependencies
from obspy import Stream, Trace
from scipy.signal.windows import tukey

# Local files
from crotalus.dsp.filter import butter_bandpass_filter


def _pre_process(tr, decimation_factor, freqmin, freqmax, order, multiple):
    tr.detrend()
    if decimation_factor != 1:
        tr.decimate(decimation_factor)
    tr.data *= multiple
    butter_bandpass_filter(tr, freqmin, freqmax, order)


def pre_process(st, decimation_factor, freqmin, freqmax, order, multiple):
    st.merge()
    st.remove_response()

    if isinstance(st, Trace):
        _pre_process(st, decimation_factor, freqmin, freqmax, order, multiple)
    elif isinstance(st, Stream):
        for tr in st:
            _pre_process(
                tr, decimation_factor, freqmin, freqmax, order, multiple
            )


