import math
import numpy as np
from numba import njit


@njit(cache=True)
def get_filter(M, K, BetaOrder, n, Cos, CosSize):
    # Extract necessary attributes from the wdm
    B = math.pi / K
    A = (K - M) * math.pi / (2.0 * K * M)
    K2 = K ** 2
    gNorm = math.sqrt(2 * M) / math.pi

    # Initialize the filter array
    filter = np.zeros(n)

    # Get the Fourier array
    Fourier = Cos[BetaOrder]
    nFourier = CosSize[BetaOrder]
    fourier = np.copy(Fourier)

    # Calculate filter coefficients
    filter[0] = (A + fourier[0] * B) * gNorm
    fNorm = filter[0] ** 2
    fourier[0] /= math.sqrt(2)

    for i in range(1, n):
        di = float(i)
        i2 = di * di
        sumEven = 0
        sumOdd = 0

        # Calculating the sums for even and odd
        for j in range(nFourier):
            if i % K:
                pass
            elif j == i // K:
                continue
            coeff = di / (i2 - j ** 2 * K2)
            if j & 1:
                sumOdd += coeff * fourier[j]
            else:
                sumEven += coeff * fourier[j]

        # Calculating intAB
        intAB = 0
        if i % K == 0 and i // K < nFourier:
            intAB = fourier[i // K] * B / 2 * math.cos(i * A)

        intAB += 2 * (sumEven * math.sin(i * B / 2) * math.cos(i * math.pi / (2 * M)) -
                      sumOdd * math.sin(i * math.pi / (2 * M)) * math.cos(i * B / 2))

        filter[i] = gNorm * (math.sin(i * A) / di + math.sqrt(2) * intAB)
        fNorm += 2 * filter[i] ** 2

    return filter
