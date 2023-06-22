from condor_scheduler import CondorScheduler
import numpy as np
from data_models import Model
from hdiv import single_test_hdiv

exp_mean = 10
signal_mean = 53
signal_std = 10  

def main():
    condor_scheduler = CondorScheduler(
            output_folder="test_outputs",
            input_folder="../../HDiv",
           
            prologue=[
                "ls",
                "pwd",
                "cd HDiv",
                "ls",
                "pwd",
                "cd Build_gc11",
                "ls",
                "pwd",
                "hostname",
            ],
        )
    
    sample_fraction = [0.0,0.01,0.03,0.05,0.10]
    samplesize = [100]#[100,300,500,1000,3000,5000,10000,20000]
 #   samplesize = [300,700,5000]
    rounds = 1
    numberoftoys = 1
    #For testing the Number of Bins
#    Binsize = range(1,70,4)

    for sf in sample_fraction:
        total_data = 2000
        signal_size = int(total_data * sf)       
        ref_model = Model(is_data=False, size=total_data)
        data_model = ref_model.get_data_sample(signal_size=signal_size,mu=signal_mean,sigma=signal_std)
        single_test_hdiv(total_data, signal_size, ref_model, data_model,exp_mean,signal_mean,signal_std)
        for ss in samplesize:   
            for i in range(rounds):
                condor_scheduler.submit_task("./computation.py",[ss,sf,numberoftoys])
            condor_scheduler.finalise()


if __name__ == "__main__":
    main()
