#!/bin/zsh
RELEASE=release-05-00-01

source /cvmfs/belle.cern.ch/tools/b2setup
b2setup $RELEASE

# Deal with segmentation violation for some versions
export LD_LIBRARY_PATH=/sw/belle/local/neurobayes/lib/:$LD_LIBRARY_PATH

# Running on data for exp 31-65
export USE_GRAND_REPROCESS_DATA=1

# Set Belle DB
export BELLE_POSTGRES_SERVER=can01

# Access to Belle DB
export PGUSER=g0db

