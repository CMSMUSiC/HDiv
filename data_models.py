import numpy as np
import hist
from hist import Hist
import math


class Model:
    def __init__(
        self,
        is_data: bool,
        size: int,
        sample_size: int = 1000,
    ):
        # Constant parameters
        self.num_syst = 3
        self.sample_size = sample_size
        # Histograms
        self.nbins = 30
        self.x_min = 0
        self.x_max = 60
        # Background Model
        self.beta = 10
        # Signal Model
        # self.mu = (self.x_max + self.x_min) / 2.0
        self.mu = 40
        # self.mu = 10
        self.sigma = 15

        # Model specific
        self.is_data = is_data
        self.size = size
        # self.signal_size = signal_size
        # if self.signal_size >= self.size:
        #     raise ValueError(
        #         f"ERROR: Invalid signal size ({self.signal_size}). Should be < background size ({self.size})."
        #     )
        # self.background_fraction = 1.0 - self.signal_fraction
        # self.signal_size = math.floor(self.size * self.signal_fraction)
        self.background_size = self.size

        # build model
        _histo = Hist.new.Regular(self.nbins, self.x_min, self.x_max, name="x").Double()
        _histo.fill(
            np.concatenate(
                [
                    # np.random.normal(self.mu, self.sigma, self.signal_size),
                    np.random.exponential(self.beta, self.background_size),
                ]
            )
        )
        self.values = _histo.values()
        self.bins = _histo.axes.edges[0]

        # calculate uncertanties
        self.stats_uncert = np.sqrt(self.values)
        # self.normalized_stats_variations = np.random.normal(size=(self.sample_size, 1))
        # self.stats_uncert[self.stats_uncert == 0] = 1
        self.syst_uncert = []
        self.normalized_syst_variations = []
        self.normalized_syst_variations_for_data_sampling = []
        if not is_data:
            for i in range(self.num_syst):
                self.syst_uncert.append(self.stats_uncert / (i + 4))
                self.normalized_syst_variations.append(
                    np.random.normal(size=(self.sample_size, 1))
                )
                self.normalized_syst_variations_for_data_sampling.append(
                    np.random.normal(size=(1, 1))
                )

    def sample(self, is_data=False):
        normalized_systs = self.normalized_syst_variations
        if is_data:
            normalized_systs = self.normalized_syst_variations_for_data_sampling

        if not self.is_data:
            new_values = np.reshape(self.values, (1, self.values.shape[0]))
            for idx_syst, syst in enumerate(self.syst_uncert):
                new_values = (
                    new_values
                    + np.reshape(syst, (1, syst.shape[0])) * normalized_systs[idx_syst]
                )
            return np.random.poisson(
                np.max([new_values, np.zeros_like(new_values)], axis=0)
            )
        raise ValueError("ERROR: Can not sample from data model.")

    @property
    def total_uncert(self):
        if self.is_data:
            return self.stats_uncert
        squared_sum = self.stats_uncert * self.stats_uncert
        for syst in self.syst_uncert:
            squared_sum += syst * syst

        return np.sqrt(squared_sum)

    def get_data_sample(self, signal_size=0):
        # build signal
        _histo = Hist.new.Regular(self.nbins, self.x_min, self.x_max, name="x").Double()
        _histo.fill(
            np.random.normal(self.mu, self.sigma, signal_size),
            # np.random.exponential(self.sigma, signal_size),
        )
        sampled_data = self.sample(is_data=True).flatten() + _histo.values()
        data_sample = Model(is_data=True, size=sampled_data.shape[0])
        data_sample.values = sampled_data
        data_sample.stats_uncert = np.sqrt(data_sample.values)
        return data_sample
