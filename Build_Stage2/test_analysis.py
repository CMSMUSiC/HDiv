from condor_scheduler import CondorScheduler
import numpy as np
import roothelpers
import ROOT
from ectools.register import ecroot
from ectools.misc import rremove
import logging


logger = logging.getLogger("scan-submitter")
   

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
                "cd Build_Stage2",
                "ls",
                "pwd",
                "hostname",
            ],
        )
    
    n_rounds = 10
    mc_root_file_name = "Build_Stage2/Lucas/bg.root"
    mc_root_file = ROOT.TFile.Open("Build_Stage2/Lucas/bg.root")
    signal_file_name = "Build_Stage2/Lucas/bg_2000.root"
    signal_file = ROOT.TFile.Open("Build_Stage2/Lucas/bg_2000.root")


    signal_names = [key.GetName() for key in signal_file.GetListOfKeys()]
    mc_names = [key.GetName() for key in mc_root_file.GetListOfKeys()]


    for mc_name in mc_names:
        if not mc_name in signal_names:
            err_msg = "Class %s only in mc file but missing in signal file" % mc_name
            logger.error(err_msg)
            err_msg = "Maybe you forgot to merge background and signal "
            err_msg += "or merged with --filter option ?"
            logger.error(err_msg)
            raise RuntimeError(err_msg)
        
    i = 0
    mc_root_file.Close("Build_Stage2/Lucas/bg.root")
    signal_file.Close("Build_Stage2/Lucas/bg_2000.root")    

    for ec_name in mc_names:
        condor_scheduler.submit_task("./computation.py",[ec_name,n_rounds,mc_root_file,signal_file])
        if(i == 5 ): break
        i = i+1
    condor_scheduler.finalise(   

if __name__ == "__main__":
    main()
