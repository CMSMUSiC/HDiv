# H-Div 

Play ground of MUSiC implementation of H-Div as test statistics for discovery.

## H-Div Original paper

Comparing Distributions by Measuring Differences that Affect Decision Making

https://openreview.net/pdf?id=KB5onONJIAU

## Setup
First get the git repository:
`git clone https://github.com/CMSMUSiC/HDiv.git`



`source set_env.sh`

Create a new Build folder:
`mkdir Build_name`
`cd Build_name`

`cmake ..`
`ninja `
`ninja lut`
`ninja install`

## Most important Files
#   music data test.py
This is the file which is used to perform the Scann. Here you need to specify
the Rootfiles you want to use as Input (Ln 483 f.).
When you call this script you further specify the number of Rounds, toys and
cores.
#   plot p vals.py
This is the main plotting script.
#   Get Eventlist.py
This is the function you call to get the specified classes. This script calls
get event classes.py, where you can specify which classes are selected. The
classes are further sorted by occupancy
