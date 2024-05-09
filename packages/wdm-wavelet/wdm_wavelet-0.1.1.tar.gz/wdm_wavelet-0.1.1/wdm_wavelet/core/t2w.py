import numpy as np
from numpy.fft import fft
from numba import njit


@njit(cache=True)
def t2w(M, m_H, WWS, filter, MM):
    """
    Transform time series to WDM

    :param M: max layers
    :param m_H:
    :param WWS: time series
    :param nWWS: length of time series
    :param filter: filter coefficients
    :param MM:  MM = 0 requests power map of combined quadratures (not amplitudes for both)
    :return:
    """

    M1 = M + 1
    M2 = M * 2
    nWDM = m_H
    nTS = len(WWS)
    KK = MM

    if MM <= 0:
        MM = M

    # adjust nWWS to be a multiple of MM
    nWWS = len(WWS)
    # this->nWWS += this->nWWS%MM ? MM-this->nWWS%MM : 0;
    nWWS += MM - nWWS % MM if nWWS % MM else 0

    # initialize time series with boundary conditions (mirror)
    m = nWWS + 2 * nWDM
    ts = np.zeros(m)

    for n in range(nWDM):
        ts[nWDM - n] = WWS[n]
    for n in range(nTS):
        ts[nWDM + n] = WWS[n]
    for n in range(int(m - nWDM - nTS)):
        ts[n + nWDM + nTS] = WWS[nTS - n - 1]

    # create symmetric arrays
    wdm = filter[:nWDM]
    # INV = np.array(filter[nWDM - 1::-1])

    # WDM = INV[::-1]

    # reallocate TF array
    N = int(nWWS / MM)
    L = 2 * N * M1 if KK < 0 else N * M1
    m_L = m_H if KK < 0 else 0

    pWDM = np.zeros(L)  # Assuming pWWS is a numpy array

    odd = 0
    sqrt2 = np.sqrt(2)

    for n in range(N):
        # create references
        map00 = pWDM[n * M1:]
        map90 = pWDM[(N + n) * M1:]
        pTS = ts[nWDM + n * MM:]

        re = np.zeros(M2)
        im = np.zeros(M2)

        J = M2
        for j in range(0, nWDM - 1, M2):
            J = M2 + j
            pTS_inv = ts[nWDM + n * MM - J:]
            for m in range(M2):
                re[m] += pTS[j + m] * wdm[j + m] + pTS_inv[m] * wdm[J - m]

        re[0] += wdm[J] * pTS[J]

        # Perform FFT
        fft_result = fft(re)
        re, im = fft_result.real, fft_result.imag

        re[0] = im[0] = re[0] / sqrt2
        re[M] = im[M] = re[M] / sqrt2

        if KK < 0:
            for m in range(M + 1):
                if (m + odd) & 1:
                    map00[m] = sqrt2 * im[m]
                    map90[m] = sqrt2 * re[m]
                else:
                    map00[m] = sqrt2 * re[m]
                    map90[m] = -sqrt2 * im[m]
        else:  # power map
            map00[:M + 1] = re[:M + 1] ** 2 + im[:M + 1] ** 2

        odd = 1 - odd

    return m_L, nWWS, pWDM.reshape(2, N, M1)
