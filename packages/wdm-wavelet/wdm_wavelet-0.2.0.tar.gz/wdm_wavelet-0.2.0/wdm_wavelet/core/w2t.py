from numba import njit
import numpy as np
from numpy.fft import ifft


def w2t(tf_map, m_Layer, filter):
    """
    Inverse transform from WDM to time series.

    :param tf_map: The transformed frequency map (numpy array).
    :param m_Layer: The maximum number of layers.
    :param nWWS: Number of points in the WDM map.
    :param m_H: Number of harmonics.
    :param filter: Wavelet decomposition filter coefficients.
    :return: Modified original time series.
    """
    nWDM = len(filter)
    nWWS = tf_map.size
    M = m_Layer - 1
    M1 = M + 1
    M2 = M * 2
    N = nWWS // (M2 + 2)
    nTS = M * N + 2 * nWDM
    sqrt2 = np.sqrt(2.)
    reX = np.zeros(M2)
    imX = np.zeros(M2)
    wdm = np.array(filter)

    # if M * N / len(tf_map) != 1:
    #     print("Inverse is not defined for the up-sampled map")
    #     raise ValueError("Inverse operation not defined.")

    ts = np.zeros(nTS, dtype=tf_map.dtype)

    for n in range(N):
        reX[:] = 0
        imX[:] = 0
        for j in range(1, M):
            if (n + j) & 1:
                imX[j] = tf_map[n * M1 + j] / sqrt2
            else:
                if j & 1:
                    reX[j] = -tf_map[n * M1 + j] / sqrt2
                else:
                    reX[j] = tf_map[n * M1 + j] / sqrt2

        if (n & 1) == 0:
            reX[0] = tf_map[n * M1]
        if ((n + M) & 1) == 0:
            if M & 1:
                reX[M] = -tf_map[n * M1 + M]
            else:
                reX[M] = tf_map[n * M1 + M]

        result = ifft(np.vectorize(complex)(reX, imX), n=M2)
        reX = result.real * 2 * len(result)

        m = M * (n & 1)
        mm = m

        ts[nWDM + n * M] += wdm[0] * reX[m]
        for j in range(1, nWDM):
            m += 1
            if m == 2 * M:
                m = 0
            ts[nWDM + n * M + j] += wdm[j] * reX[m]
            if mm == 0:
                mm = 2 * M - 1
            else:
                mm -= 1
            ts[nWDM + n * M - j] += wdm[j] * reX[mm]

    return ts[nWDM:-nWDM]
