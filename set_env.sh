# This is a set_env script
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
   
# source /cvmfs/sft.cern.ch/lcg/views/LCG_102b/x86_64-centos7-gcc11-dbg/setup.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_102b/x86_64-centos7-gcc11-opt/setup.sh
#source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh

export CMAKE_GENERATOR=Ninja


export SCAN_BASE=$SCRIPTDIR


# set PATH
export PATH=$PATH:$SCRIPTDIR/bin;

cd $SCRIPTDIR/tools/
source set_env.sh

cd $SCRIPTDIR/MUSiC-Utils/
source set_env.sh

cd $SCRIPTDIR
