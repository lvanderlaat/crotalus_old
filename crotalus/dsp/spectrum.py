# Python Standard Library

# Other dependencies
import numpy as np
from scipy.fft import rfft
from scipy.signal.windows import tukey

# Local files



def get_linear_bands(f_lower, f_upper, f_delta):
    """ Get linear frequency spectrum bands

    To downsample spectrum

    Parameters
    ----------
    f_lower : float
        Lower frequency
    f_upper : float
        Upper frequency
    f_delta : float
        Frequency bin width

    Returns
    -------
    fl : np.ndarray
        Lower frequency array
    fc : np.ndarray
        Center frequency array
    fu : np.ndarray
        Upper frequency array
    """
    fl = np.arange(f_lower, f_upper, f_delta)
    fu = np.arange(f_lower+f_delta, f_upper+f_delta, f_delta)
    fc = (fl + fu)/2
    return fl, fc, fu


def get_8ve_bands(sampling_rate, fraction, f_lower, f_upper):
    """ Get octave frequency spectrum bands

    For better resolution in low frequency

    Parameters
    ----------
    sampling_rate : float
        Trace sampling frequency
    fraction : float
        Octave fraction to use
    f_lower : float
        Lower frequency
    f_upper : float
        Upper frequency

    Returns
    -------
    fl : np.ndarray
        Lower frequency array
    fc : np.ndarray
        Center frequency array
    fu : np.ndarray
        Upper frequency array
    """
    octs = np.log2(f_upper/f_lower)
    bmax = np.ceil(octs/fraction)

    fc = f_lower*2**(np.arange(bmax)*fraction)
    fl = fc*2**(-fraction/2)
    fu = fc*2**(+fraction/2)
    return fl, fc, fu


def spectrum(tr, pad):
    f  = np.fft.rfftfreq(tr.stats.npts, tr.stats.delta)
    Sx = np.abs(rfft(tr.data))
    Sx *= tukey(Sx.shape[0], alpha=pad) # taper
    return f, Sx


def spectrogram(tr, window_length, overlap, pad,):
    """Seismic Spectral Amplitude Measurement (SSAM)

    Seismic Spectral Amplitude Measurement (SSAM)

    For multiple resamplings a list for `fl` and `fu` can be passed, a list of
    SSAM matrices will be returned. This is useful to get both a linear SSAM
    and a octave SSAM in the frequency range.

    Parameters
    ----------
    tr : obspy.trace
        Raw seimic trace
    window_length : float
        Window length in seconds
    overlap : float
        Overlap fraction between windows (0-1)
    pad : float
        Taper pad fraction (0-1)

    Returns
    -------
    utcdatetimes : array of obspy.UTCDateTime objects
        Time for each data point
    f : np.ndarray
        Frequency (1d) array
    Sx : tuple of np.ndarray or np.ndarray
        SSAM matrix or matrices

    """
    utcdatetimes, data_windowed = st2windowed_data(tr, window_length, overlap)
    data_windowed = data_windowed[0]

    data_windowed *= tukey(data_windowed.shape[1], alpha=pad) # taper

    Sxx = np.abs(rfft(data_windowed))

    f = np.fft.rfftfreq(data_windowed.shape[1], tr.stats.delta)
    return utcdatetimes, f, Sxx


def downsample_spectrogram(
    f, Sx, f_lower, f_upper, method='octave', f_delta=0.25, fraction=1/12,
    sampling_rate=None
):
    """ Resample spectrogram

    Downsample spectrogram to SSAM. Uses the mean in each frequency bin

    Parameters
    ----------
    f : np.ndarray
        Frequency array of the spectrum
    Sx : np.ndarray
        Spectrum or spectrogram array
    f_lower : float
        Lower frequency
    f_upper : float
        Upper frequency
    method : str
        'octave' or 'linear'
    f_delta : float
        Frequency bin width, to use with method='linear'
    fraction : float
        Octave fraction, to use with method='octave'
    sampling_rate : float
        To use with method='octave'

    Returns
    -------
    ssam : np.ndarray
        Downsampled spectrogram amplitude array

    """
    if method == 'octave':
        fl, fc, fu = get_8ve_bands(sampling_rate, fraction, f_lower, f_upper)
    elif method == 'linear':
        fl, fc, fu = get_linear_bands(f_lower, f_upper, f_delta)

    if Sx.ndim == 1:
        ssam = np.empty(len(fl))
        for i in range(len(fl)):
            freq_min_idx = (np.abs(f - fl[i])).argmin()
            freq_max_idx = (np.abs(f - fu[i])).argmin()
            ssam[i] = Sx[freq_min_idx:freq_max_idx+1].mean()
    elif Sx.ndim == 2:
        Sxx = Sx
        ssam = np.empty((Sxx.shape[0], len(fl)))
        for i in range(len(fl)):
            freq_min_idx = (np.abs(f - fl[i])).argmin()
            freq_max_idx = (np.abs(f - fu[i])).argmin()
            ssam[:, i] = Sxx[:, freq_min_idx:freq_max_idx].mean(axis=1)
    return fc, ssam
