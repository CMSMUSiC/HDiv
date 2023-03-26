import numpy as np
import hist
from hist import Hist
import math


class Model:
    def __init__(
        self,
        is_data: bool,
        size: int,
        signal_fraction: float = 0,
    ):
        # Constant parameters
        self.num_syst = 3
        # Histograms
        self.nbins = 70
        self.x_min = 0
        self.x_max = 100
        # Background Model
        self.beta = 10
        # Signal Model
        self.mu = (self.x_max + self.x_min) / 2.0
        self.sigma = 1

        # Model specific
        self.is_data = is_data
        self.size = size
        self.signal_fraction = signal_fraction
        if self.signal_fraction >= 1:
            raise ValueError(
                f"ERROR: Invalid singal fraction ({self.signal_fraction}). Should be < 1."
            )
        self.background_fraction = 1.0 - self.signal_fraction
        self.signal_size = math.floor(self.size * self.signal_fraction)
        self.background_size = self.size - self.signal_size

        # build model
        _histo = Hist.new.Regular(self.nbins, self.x_min, self.x_max, name="x").Double()
        _histo.fill(
            np.concatenate(
                [
                    np.random.normal(self.mu, self.sigma, self.signal_size),
                    np.random.exponential(self.beta, self.background_size),
                ]
            )
        )
        self.values = _histo.values()
        self.bins = _histo.axes.edges[0]

        # calculate uncertanties
        self.stats_uncert = np.sqrt(self.values)
        self.stats_uncert[self.stats_uncert == 0] = 1
        self.syst_uncert = []
        for i in range(self.num_syst):
            self.syst_uncert.append(self.stats_uncert / (i + 4))

    def sample(self, sample_size):
        if not self.is_data:
            new_values = np.reshape(self.values, (1, self.values.shape[0]))
            for syst in self.syst_uncert:
                new_values = new_values + np.reshape(
                    syst, (1, syst.shape[0])
                ) * np.random.normal(size=(sample_size, syst.shape[0]))
            new_values = new_values + np.reshape(
                self.stats_uncert, (1, self.stats_uncert.shape[0])
            ) * np.random.normal(size=(sample_size, self.stats_uncert.shape[0]))
            return np.random.poisson(
                np.max([new_values, np.zeros_like(new_values)], axis=0)
            )
        raise ValueError("ERROR: Can not sample from data model.")

    @property
    def total_uncert(self):
        squared_sum = self.stats_uncert * self.stats_uncert
        for syst in self.syst_uncert:
            squared_sum += syst * syst

        return np.sqrt(squared_sum)
