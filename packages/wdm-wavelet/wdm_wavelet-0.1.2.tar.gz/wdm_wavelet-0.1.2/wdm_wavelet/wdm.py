from .core.get_filter import get_filter
from .core.t2w import t2w
from .fourier_coeff import load_fourier_coeff
from gwpy.timeseries import TimeSeries
from wdm_wavelet.types import TimeFrequencyMap


class WDM:
    """
    WDM class
    """

    def __init__(self, M, K, beta_order, precision):
        self.M = M
        self.K = K
        self.beta_order = beta_order
        self.precision = precision

        Cos, Cos2, SinCos, CosSize, Cos2Size, SinCosSize = load_fourier_coeff()

        n_max = int(3e5)
        filter = get_filter(M, K, beta_order, n_max, Cos, CosSize)

        residual = 1 - filter[0] ** 2
        prec = 10 ** (-precision)

        N = 1
        M2 = M * 2
        while residual > prec or (N - 1) % M2 or N // M2 < 3:
            residual -= 2 * filter[N] ** 2
            N += 1

        self.filter = filter[:N]
        self.m_H = N

    def t2w(self, strain, sample_rate=None, t0=0, MM=-1):
        """
        Transform time series to WDM


        Parameters
        ----------
        strain: array-like, TimeSeries
            Time series data

        sample_rate: float, optional
            Sample rate of the time series data. Required if strain is not a TimeSeries object

        t0: float, optional
            Start time of the time series data. Default is 0

        MM: int, optional
            MM = 0 requests power map of combined quadratures (not amplitudes for both)
        """

        # convert to plain numpy array for numba compatibility
        if isinstance(strain, TimeSeries):
            sample_rate = strain.sample_rate.value
            t0 = strain.t0.value
            strain = strain.value
        elif str(type(strain)) == "<class 'pycbc.types.timeseries.TimeSeries'>":
            try:
                sample_rate = strain.sample_rate
                t0 = float(strain.start_time)
                strain = strain.data
            except AttributeError:
                raise ValueError("strain is detected as a pycbc TimeSeries object, "
                                 "but the sample_rate or start_time cannot be extracted")
        else:
            if sample_rate is None:
                raise ValueError("sample_rate must be provided if strain is not"
                                 " a gwpy.TimeSeries object or a pycbc.TimeSeries object")

        # calculate the time frequency map
        _, _, time_frequency_map = t2w(self.M, self.m_H, strain, self.filter, MM)

        # calculate the df and dt
        max_f_layer = time_frequency_map.shape[2] - 1
        max_t_layer = time_frequency_map.shape[1]
        df = sample_rate/max_f_layer/2.

        t_len = len(strain) / sample_rate
        dt = t_len/max_t_layer

        time_frequency_map = time_frequency_map[0] - 1j * time_frequency_map[1]

        return TimeFrequencyMap(time_frequency_map.T, df, dt, t0)

    def w2t(self):
        raise NotImplementedError("w2t is not implemented yet")