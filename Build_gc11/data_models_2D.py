import numpy as np
import math

#The Modell for the 2D Jensen shannonn data
class Model_2D:
    def __init__(
        self,
        is_data: bool,
        size: int,
        sample_size: int = 2000,  
    ):
        # Constant parameters
        self.num_syst = 1
        self.sample_size = sample_size

        # Histograms
        self.nbins = 5
        self.x_min = 0
        self.x_max = 60 
        self.y_min = 0
        self.y_max = 60     

        # Background Model
        self.beta = 10

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

        #Assume uncorrelated and identical background
        X = np.random.exponential(self.beta, self.background_size)
        Y = np.random.exponential(self.beta, self.background_size)
        # build model
        background_hist, xedges, yedges = np.histogram2d(X, Y, bins=(self.nbins,self.nbins), range=[[self.x_min,self.x_max],[self.y_min,self.y_max]], density=None, weights=None)
        background_hist = background_hist.T
        self.values = background_hist
        self.xbins = xedges
        self.ybins = yedges

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
        #The 2D creation of toys

        normalized_systs = self.normalized_syst_variations
        if is_data:
            normalized_systs = self.normalized_syst_variations_for_data_sampling
        result = []

        for idx_syst, syst in enumerate(self.syst_uncert):
            if not self.is_data:
                for systs in normalized_systs[idx_syst]:
                    toy = []
                    for i in range(self.nbins):  
                        new_values = np.reshape(self.values[i], (1, self.values[i].shape[0]))
                        new_values = (
                            new_values
                            + np.reshape(syst[i], (1, syst[i].shape[0])) * systs
                        )
                        toy.append( np.random.poisson(
                            np.max([new_values, np.zeros_like(new_values)], axis=0)
                        ))
                    result.append(np.reshape(toy ,(self.nbins,self.nbins)))      
                       
            else: 
                raise ValueError("ERROR: Can not sample from data model.")   
             
        return result 
    
    def sample_1D(self,values_1d,is_data=False):
        
        if is_data:
            normalized_systs = self.normalized_syst_variations_for_data_sampling
        result = []



        #Recalculate of the uncertanties for the 1D Modell
        stats_uncert = np.sqrt(values_1d)

        syst_uncert = []
        normalized_syst_variations = []
        normalized_syst_variations_for_data_sampling = []
        if not is_data:
            for i in range(self.num_syst):
                syst_uncert.append(stats_uncert / (i + 4))
                normalized_syst_variations.append(
                    np.random.normal(size=(self.sample_size, 1))
                )
                normalized_syst_variations_for_data_sampling.append(
                    np.random.normal(size=(1, 1))
                )


        normalized_systs = normalized_syst_variations

        if not self.is_data:
            new_values = np.reshape(values_1d, (1, values_1d.shape[0]))
            for idx_syst, syst in enumerate(syst_uncert):
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

    def get_data_sample(self,mu,sigma, signal_size=0):
        # build signal
        Signal = np.random.multivariate_normal(mean=mu,cov=sigma,size=signal_size)

        Signal_hist, xedges, yedges = np.histogram2d(Signal[:,0], Signal[:,1], bins=(self.nbins,self.nbins), range=[[self.x_min,self.x_max],[self.y_min,self.y_max]], density=None, weights=None)
        Signal_hist = Signal_hist.T

        combined_hist = self.values + Signal_hist

        return combined_hist
