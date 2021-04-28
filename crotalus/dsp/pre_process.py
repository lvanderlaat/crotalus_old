# Python Standard Library

# Other dependencies
from obspy import Stream, Trace
from scipy.signal.windows import tukey

# Local files
from crotalus.dsp.filter import butter_bandpass_filter


def _pre_process(tr, decimation_factor, freqmin, freqmax, order, pad):
    tr.detrend()
    tr.decimate(decimation_factor)
    butter_bandpass_filter(tr, freqmin, freqmax, order)
    # tr.data *= tukey(tr.stats.npts, alpha=pad)


def pre_process(st, decimation_factor, freqmin, freqmax, order, pad):
    if isinstance(st, Trace):
        _pre_process(st, decimation_factor, freqmin, freqmax, order, pad)
    elif isinstance(st, Stream):
        for tr in st:
            _pre_process(tr, decimation_factor, freqmin, freqmax, order, pad)


