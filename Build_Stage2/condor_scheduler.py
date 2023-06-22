#!/usr/bin/env python3

import os
import datetime
import json
import getpass


class CondorScheduler:
    def __init__(self, output_folder="", input_folder="", prologue=""):
        self.prologue = prologue
        if prologue != "":
            self.prologue = "; ".join(prologue)
        self.job_id_to_args = {}
        self.job_id = 0
        self.current_dir = os.getenv("PWD")
        if output_folder == "":
            output_folder = os.getenv("PWD")

        now = datetime.datetime.now()
        self.output_file_path = (
            f"{output_folder}/outputs_{now.strftime('%Y_%m_%d_%H_%M_%S')}"
        )

        os.mkdir(self.output_file_path)

        self.input_folder = input_folder
        if self.input_folder != "":
            print("Packing input files ...")
            os.system(r"rm task.tar.gz > /dev/null 2>&1")
            tar_command = r'tar --exclude="*.log" --exclude="crab.log" --exclude="Build" --exclude="Results"  --exclude="parallelbar" --exclude="gifs" --exclude="test" --exclude="test_parallel" --exclude="test_outputs" --exclude="outputs"  --exclude="task.tar.gz" --exclude="__pycache*" --exclude="build" --exclude="docs_BKP" --exclude="docs" --exclude="*.root" --exclude="NanoMUSiC/MUSiC-CRAB/crab_nano_music*" -zcvf task.tar.gz __TAR_FOLDER__/*'
            tar_command = tar_command.replace("__TAR_FOLDER__", input_folder)
            os.system(tar_command)
            print("")

    def submit_task(self, executable_script, arguments):
        if not isinstance(arguments, list):
            arguments = [arguments]

        base_jdl = """
	universe     = vanilla
	getenv       = true
	executable   = __EXECUTABLE__
	LogDirectory= __LOG__
	log          = $(LogDirectory)/condor-$(CLUSTER)_$(PROCESS).log
	Output       = $(LogDirectory)/condor.out
	Error        = $(LogDirectory)/condor.err
#    should_transfer_files = true
#    transfer_output_files = dummy_output.txt        
#    transfer_output_remaps = "dummy_output.txt=logs/$(LogDirectory)/dummy_output.txt"
	Stream_Output = true
	Stream_Error = true
	requirements = Machine != "lx1b00.physik.rwth-aachen.de"
	request_memory=1300
	rank = Memory
	notification = never          
	queue
	"""
#    should_transfer_files = true
#    transfer_output_files = dummy_output.txt        
#   transfer_output_remaps = "dummy_output.txt=logs/$(LogDirectory)/dummy_output.txt"

        base_jdl = base_jdl.replace(
            "__LOG__", f"{self.output_file_path}/job_id_{self.job_id}"
        )
        string_arguments = []
        for var in arguments:
            string_arguments.append(str(var))
#        executable = f"mkdir -p /user/scratch/{getpass.getuser()}; cd /user/scratch/{getpass.getuser()}; working_dir=$RANDOM; mkdir $working_dir; cd $working_dir;"
        executable = f"cd $_CONDOR_SCRATCH_DIR;"
        if self.input_folder != "":
            executable += (
                f"/net/software_t2k/tools/cccp/cccp {self.current_dir}/task.tar.gz .; "
            )
            executable += r"tar -zxf task.tar.gz;"

        executable += f"{self.prologue}; "
        executable += f"{executable_script} {' '.join(string_arguments)};"
      #  executable += r"touch dummy_output.txt;"
        executable += r"rm -rf $working_dir > /dev/null 2>&1"

        os.mkdir(f"{self.output_file_path}/job_id_{self.job_id}")
        with open(
            f"{self.output_file_path}/job_id_{self.job_id}/executable.sh", "w"
        ) as f:
            f.write(executable)
        os.system(
            f"chmod +x {self.output_file_path}/job_id_{self.job_id}/executable.sh"
        )

        base_jdl = base_jdl.replace(
            "__EXECUTABLE__",
            f"{self.output_file_path}/job_id_{self.job_id}/executable.sh",
        )
        with open(f"{self.output_file_path}/job_id_{self.job_id}/condor.jdl", "w") as f:
            f.write(base_jdl)

        self.job_id_to_args[self.job_id] = {}
        self.job_id_to_args[self.job_id]["results"] = ""
        self.job_id_to_args[self.job_id]["args"] = [executable_script]
        for arg in arguments:
            self.job_id_to_args[self.job_id]["args"].append(str(arg))
        os.system(
            f"condor_submit {self.output_file_path}/job_id_{self.job_id}/condor.jdl"
        )
        self.job_id += 1

    def finalise(self):
        with open(f"{self.output_file_path}/job_id_to_args.json", "w") as f:
            json.dump(self.job_id_to_args, f)

    @classmethod
    def harvest(cls, output_path):
        
        with open(f"{output_path}/job_id_to_args.json") as f:
            job_id_to_args = json.load(f)

        for id in job_id_to_args:
            if(int(id) % 10 == 0): print(id)
            with open(f"{output_path}/job_id_{id}/condor.out") as f:
                #Checking return code:
                folder_path = f"{output_path}/job_id_{id}"
                file_extension = '.log'  # replace with your desired file extension
                file_extension2 = '.err'
                # iterate through all files in the folder
                for file_name in os.listdir(folder_path):
                    # check if the file has the desired extension
                    if file_name.endswith(file_extension):
                        # construct the full file path
                        file_path = os.path.join(folder_path, file_name)
                        # read in the file contents
                        with open(file_path, 'r') as l:
                            file_name2 = 'condor.err'
                            file_path2 = os.path.join(folder_path, file_name2)
                            with open(file_path2, 'r') as e:
                                et = e.read()
                                if(('Normal termination (return value 0)' in l.read()) 
                                   and ( 'returned status 2' not in et) 
                                   and ( 'Traceback' not in et) 
                                   and ( 'No space' not in et) 
                                   and ( 'RuntimeWarning' not in et) 
                                   and('tar: Error is not recoverable' not in et)
                                   ):
                                    job_id_to_args[id]["results"] = f.read().split("\n")[-2]
                                    break
                                else: 
                                    print("error in ",id )
                                    job_id_to_args[id]["results"] = "NaN"
                                    break
                            

        with open(f"{output_path}/job_id_to_args.json", "w") as f:
            json.dump(job_id_to_args, f)

        return job_id_to_args
