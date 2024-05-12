from dataclasses import dataclass
import numpy as np


@dataclass
class TimeFrequencyMap:
    """
    Time-frequency map data class

    Parameters
    ----------
    data: np.ndarray
        Complex Time-frequency map data
    df: float
        Frequency resolution
    dt: float
        Time resolution
    t0: float
        Start time
    """
    data: np.ndarray
    df: float
    dt: float
    t0: float

    @property
    def n_freq(self):
        """
        Number of frequency bins

        Returns
        -------
        int
        """
        return self.data.shape[0]

    @property
    def n_time(self):
        """
        Number of time bins

        :returns: int
        """
        return self.data.shape[1]

    @property
    def start_time(self):
        """
        Start time

        :return: float
        """
        return self.t0

    @property
    def end_time(self):
        """
        End time

        :return: float
        """
        return self.t0 + self.n_time * self.dt

    @property
    def start_freq(self):
        """
        Start frequency

        :return: float
        """
        return 0.

    @property
    def end_freq(self):
        """
        End frequency

        :return: float
        """
        return self.df * self.n_freq

    def energy(self, low_cut=None):
        """
        Energy of the time-frequency map

        :param low_cut: float, optional
            Low cut frequency. If provided, the energy below this frequency will be set to NaN
        :return: np.ndarray
        """
        energy = np.abs(self.data)
        if low_cut is not None:
            energy = np.where(energy < low_cut, np.nan, energy)
        return energy

    def plot_energy(self, fig=None, ax=None, low_cut=None, **kwargs):
        """
        Plot the energy of the time-frequency map

        :param fig: matplotlib.figure.Figure, optional
        :param ax: matplotlib.axes.Axes, optional
        :param low_cut: float, optional
            Low cut frequency. If provided, the energy below this frequency will be set to NaN and not plotted
        :param kwargs: dict
            Additional arguments to pass to ax.imshow
        :return: matplotlib.axes.Axes
        """
        import matplotlib.pyplot as plt
        if ax is None:
            fig, ax = plt.subplots()
        im = ax.imshow(self.energy(low_cut=low_cut), aspect="auto", origin="lower",
                  extent=[self.start_time, self.end_time, self.start_freq, self.end_freq],
                  **kwargs)

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")

        fig.colorbar(im, ax=ax)
        return ax