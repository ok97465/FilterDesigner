# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License

"""."""

import numpy as np
from numpy import ndarray, arange
from numpy.fft import fft


def db2(data, db_range=60.0, db_cut=None, b_normalize=True):
    """Convert 20log10(data).

    Parameters
    ----------
    data : ndarray
        dB 변환 할 데이터
    db_range : float
        dB Dynamic Range (the default is 60.0)
    db_cut : float, optional
        dB 변환 시 최소값 (the default is None, None이면 미 수행), (b_normalize가 True 이면 Normalize 이후 cut 값)
    b_normalize : bool, optional
        최대값을 0으로 변환 여부 (the default is True)

    Returns
    -------
    ndarray
        20log10(data)
    """

    data_abs = np.abs(data)
    max_v = data_abs.max()
    db_max = 20 * np.log10(max_v)

    with np.errstate(divide='ignore'):
        db_data = 20 * np.log10(data_abs)
    db_data[db_data < (db_max - db_range)] = db_max - db_range

    if b_normalize:
        db_data -= db_max

    if db_cut:
        db_data[db_data < db_cut] = db_cut
    return db_data


def magnitude_of_frequency_response(data, fs, uprate):
    """

    Parameters
    ----------
    data: ndarray
    fs: float
        sampling frequency
    uprate: int

    Returns
    -------
    (ndarray, ndarray)
        mag_fre_db, frequnecy
    """
    mag_fre = fft(data, len(data) * uprate)
    mag_fre_db = db2(mag_fre, 90)[:len(mag_fre)//2]

    n_sample = len(mag_fre_db)
    frequency = arange(n_sample) / n_sample * fs / 2

    return mag_fre_db, frequency
