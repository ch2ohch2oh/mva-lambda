"""
Some utility functions to make your life easier.
"""
import os

B2VARIABLES = [
    'BELLE2_EXTERNALS_DIR', 
    'BELLE2_EXTERNALS_SUBSIR',
    'BELLE2_EXTERNALS_OPTION', 
    'BELLE2_EXTERNALS_VERSION',
    'BELLE2_LOCAL_DIR', 
    'BELLE2_OPTION', 
    'BELLE2_RELEASE', 
    'BELLE_POSTGRES_SERVER', 
    'USE_GRAND_REPROCESS_DATA',
    'PANTHER_TABLE_DIR', 
    'PGUSER'
]

LINE_WIDTH = 80

def print_b2env():
    """
    Print relevant BELLE2 relevant env variables to the stdout.
    """
    print('BELLE2 Environmental variables'.center(LINE_WIDTH, '='))
    for v in B2VARIABLES:
        print("%30s = %s" % (v, os.getenv(v)))
    print(''.center(LINE_WIDTH, '='))
