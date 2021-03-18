import numpy as np


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


def mean_freq(f, Sx):
    """ Mean frequency

    Carniel & Di Cecca (1999)

    Parameters
    ----------
    f : np.ndarray
        Frequency (1d) array
    Sx : np.ndarray
        One dimension Spectrum (f,) or two dimension spectra (window, f)

    Returns
    -------
    freq_mean : float or np.ndarray
        Mean frequency
    """
    if Sx.ndim == 1:
        Sx   = Sx/Sx.max()
        Stot = Sx.mean()
        Sx   = Sx/Stot
        freq_mean = (f*Sx).mean()
    elif Sx.ndim == 2:
        Sx   = Sx/Sx.max(axis=1)[:, None]
        Stot = Sx.mean(axis=1)
        Sx   = Sx/Stot[:, None]
        freq_mean = (f*Sx).mean(axis=1)
    return freq_mean


def dom_freq(f, Sx, k):
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
    freq_mean : float
        Mean frequency
    """
    if Sx.ndim == 1:
        index     = np.argpartition(-Sx, k)
        index_top = index[:k]
        freq_top  = f[index_top]
        freq_mean = freq_top.mean()
    elif Sx.ndim == 2:
        f           = np.stack([f for _ in range(Sx.shape[0])])
        indices     = np.argpartition(-Sx, k, axis=1)
        indices_top = indices[:, :k]
        freq_top    = np.take_along_axis(f, indices_top, axis=1)
        freq_mean   = freq_top.mean(axis=1)
    return freq_mean
