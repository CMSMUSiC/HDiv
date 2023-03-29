#!/bin/sh -e
set -o pipefail
echo Job started: $(date)
CESUBMITTASKNAME=Rec_2Muon+X_af9c4cbf601ea1ea31a42949941716d56a2999e6
CESUBMITCREATEDATE=2023-03-10
CESUBMITCREATEDATETIME=2023-03-10-13-24-52
CESUBMITUSERNAME=ykaiser
CESUBMITNODEID=$1
rchars=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789; CESUBMITRUNID=; for i in {1..4}; do CESUBMITRUNID=$CESUBMITRUNID${rchars:$(($RANDOM % 62)):1}; done
shift
RUNAREA=$(pwd)
echo Running in: $RUNAREA
echo Running on: $HOSTNAME
export LCG_GFAL_INFOSYS="grid-bdii.desy.de:2170,lcg-bdii.cern.ch:2170"
export MYPROXY_SERVER="grid-px0.desy.de"
export SITE_NAME="RWTH-Aachen"
export VO_CMS_DEFAULT_SE="grid-srm.physik.rwth-aachen.de"
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
export VO_DTEAM_DEFAULT_SE="grid-srm.physik.rwth-aachen.de"
export VO_OPS_DEFAULT_SE="grid-srm.physik.rwth-aachen.de"
export X509_CERT_DIR="/etc/grid-security/certificates"
export http_proxy="http://grid-squid.physik.rwth-aachen.de:3128"
export no_proxy=".rwth-aachen.de"
lsb_release  -i -r
echo Setting SCRAM_ARCH to slc7_amd64_gcc700

export SCRAM_ARCH=slc7_amd64_gcc700
export BUILD_ARCH=$SCRAM_ARCH
echo VO_CMS_SW_DIR $VO_CMS_SW_DIR
source $VO_CMS_SW_DIR/cmsset_default.sh

scram project CMSSW CMSSW_10_6_30
cd CMSSW_10_6_30
eval $(scramv1 ru -sh)
cd $RUNAREA

echo Retrieving grid packs
echo Temp $TMP
echo Vo_CMS_SW_DIR $VO_CMS_SW_DIR
#unset LD_LIBRARY_PATH;
#source /cvmfs/grid.cern.ch/umd-c7ui-latest/etc/profile.d/setup-c7-ui-example.sh;
srmcp srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/ykaiser/luigi_gridpacks/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz file://$TMP/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz
#srmcp srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/ykaiser/luigi_gridpacks/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz
#gfal-copy srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/ykaiser/luigi_gridpacks/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz
mkdir -p ./
#tar xf gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz -C ./
#rm gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz
tar xf /$TMP/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz -C ./
rm /$TMP/gridpackRec_2Muon+X_InvMass_af9c4cbf601ea1ea31a42949941716d56a2999e6.tar.gz                                    
env
echo Current directory $PWD
echo Directory content:
ls
echo $@
chmod u+x $1
echo ================= Yannik Test Start =================
echo pwd
pwd
echo ls
ls -lha
echo hostname
hostname
echo =================Yannik Test End =================  
echo Executing $@
echo ================= Start output =================
{ $@ 2>&1 1>&3 3>&- | tail -c 2M; } 3>&1 1>&2 | tail -c 3M
echo ================== End output ==================
echo Current directory $PWD
echo Directory content:
ls
echo Job ended: $(date)
