# Python Standard Library

# Other dependencies
from numba import jit
import numpy as np
from obspy import Stream
from scipy import stats

# Local files
from crotalus.dsp.filter import butter_bandpass_filter
from crotalus.dsp.obspy2numpy import st2windowed_data


def rsam(data, axis):
    """Real-time Seismic Amplitude Measure

    Endo & Murray (1991)

    Parameters
    ----------
    data : 2d np array

    Returns
    -------
    amplitude : np.ndarray
        Array of the RSEM amplitudes
    """
    amplitude = np.abs(data).mean(axis=axis)[0]
    return amplitude


@jit(nopython=True)
def rsem(data, axis=0):
    """Real-time Seismic Energy Measure

    De la Cruz-Reyna & Reyes-Dávila (2000)

    Parameters
    ----------
    data : 1d np array

    Returns
    -------
    amplitude : np.ndarray
        Array of the RSEM amplitudes

    Returns
    -------
    utcdatetimes : array of obspy.UTCDateTime objects
        Time for each data point
    amplitudes : np.ndarray
        Array of the RSEM amplitudes for each frequency band

    """

    # TODO add support for 2d array (windowed)
    # If using jit, cannot add arguments to mean
    # amplitude = np.sqrt((data**2).mean(axis=axis))

    amplitude = data**2
    amplitude = np.mean(amplitude)
    amplitude = np.sqrt(amplitude)
    return amplitude


def kurtosis(data, axis=0):
    return stats.kurtosis(data, axis=axis, fisher=False)


def dsar(tr, freqmin, freqmax, order, window_length, overlap):
    """ Displacement Seismic Amplitud Ratio

    Caudron et al. (2019)

    Parameters
    ----------
    tr : obspy.trace
        Raw seimic trace
    freqmin : list of float
        Bandpass filter minimum frequencies
    freqmax : list of float
        Bandpass filter maxmimum frequencies
    order : int
        Butterworth bandpass filter order
    window_length : float
        Window length in seconds
    overlap : float
        Overlap fraction between windows (0-1)

    Returns
    -------
    utcdatetimes : array of obspy.UTCDateTime objects
        Time for each data point
    dsar : np.array
        DSAR data
    """
    tr.integrate()
    tr.detrend()
    tr.filter('highpass', freq=0.5) # To avoid oceanic contamination

    tr_LF = tr.copy()
    tr_HF = tr.copy()

    st = Stream()
    for i, tr in enumerate([tr_LF, tr_HF]):
        tr.stats.location = i
        butter_bandpass_filter(tr, freqmin[i], freqmax[i], order)
        st += tr

    utcdatetimes, data_windowed = st2windowed_data(st, window_length, overlap)

    data_windowed = np.median(np.abs(data_windowed), axis=2)

    DSAR = data_windowed[0]/data_windowed[1]
    return utcdatetimes, DSAR


def freq_domi(f, Sx, k):
    """ Mean frequency of the top-k elements

    Girona et al. (2019)
    Takes the average frequency of the k top peaks of the spectrum

    Parameters
    ----------
    f : np.ndarray
        Frequency (1d) array
    Sx : np.ndarray
        One dimension Spectrum (f,) or two dimension spectra (window, f)
    k : int
        Number of top amplitude maxima

    Returns
    -------
    _freq_domi : float or np 1d array
        Mean frequency
    """
    if Sx.ndim == 1:
        index      = np.argpartition(-Sx, k)
        index_top  = index[:k]
        freq_top   = f[index_top]
        _freq_domi = freq_top.mean()
    elif Sx.ndim == 2:
        f           = np.stack([f for _ in range(Sx.shape[0])])
        indices     = np.argpartition(-Sx, k, axis=1)
        indices_top = indices[:, :k]
        freq_top    = np.take_along_axis(f, indices_top, axis=1)
        _freq_domi  = freq_top.mean(axis=1)
    return _freq_domi


@jit(nopython=True)
def freq_central(f, Sx):
    # TODO add support for spectrogram
    _freq_central = f[np.argsort(Sx)[len(Sx)//2]]
    return _freq_central


def freq_centroid(f, Sx):
    """ Centroid frequency

    Carniel & Di Cecca (1999)

    Parameters
    ----------
    f : np.ndarray
        Frequency (1d) array
    Sx : np.ndarray
        One dimension Spectrum (f,) or two dimension spectra (window, f)

    Returns
    -------
    _freq_centroid : float or np.ndarray
        Mean frequency
    """
    if Sx.ndim == 1:
        _freq_centroid = np.sum(Sx*f) / np.sum(Sx)
    elif Sx.ndim == 2:
        _freq_centroid = np.sum(Sx*f, axis=1) / np.sum(Sx, axis=1)
    return _freq_centroid


def freq_ratio(f, Sx, freqmin, freqmax):
    fl_min_idx = (np.abs(f - freqmin[0])).argmin()
    fl_max_idx = (np.abs(f - freqmax[0])).argmin()
    fu_min_idx = (np.abs(f - freqmin[1])).argmin()
    fu_max_idx = (np.abs(f - freqmax[1])).argmin()

    _freq_ratio = np.log(
        Sx[fu_min_idx: fu_max_idx].sum() / Sx[fl_min_idx: fl_max_idx].sum()
    )
    return _freq_ratio


@jit(nopython=True)
def tonality(Sx, k, _bin_width):
    index = np.argsort(-Sx)
    t, effective = 0, []
    for i, idx in enumerate(index):
        nxt = False
        if i > 0:
            for e in effective:
                if (idx < e+_bin_width/2) and (idx > e-_bin_width/2):
                    nxt = True
                    break
        if nxt:
            continue

        if len(effective) >= k:
            break

        left  = int(idx - _bin_width/2)
        right = int(idx + _bin_width/2)

        left_pad, right_pad = 0, 0

        if left < 0:
            left_pad = -1*left
            left = 0

        if right >= len(Sx):
            right_pad = right - len(Sx) + 1
            right = len(Sx) - 1

        Sx_slice = np.zeros(_bin_width, dtype=np.float64)

        Sx_slice[left_pad:left_pad+right-left] = Sx[left:right]

        if left_pad != 0:
            Sx_slice[:left_pad]  = np.median(Sx[left:right])
        if right_pad != 0:
            Sx_slice[-right_pad:] = np.median(Sx[left:right])

        Sx_slice = Sx_slice/Sx_slice.max()

        med = np.median(Sx_slice)

        t += (1/med)
        effective.append(idx)
    return t
