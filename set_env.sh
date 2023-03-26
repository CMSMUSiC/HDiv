# This is a set_env script
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
   
source /cvmfs/sft.cern.ch/lcg/views/LCG_102b/x86_64-centos7-gcc12-opt/setup.sh

export CMAKE_GENERATOR=Ninja


# set PATH
export PATH=$PATH:$SCRIPTDIR/bin;