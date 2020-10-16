# Dataset
# =======
# - Belle exp 55 run 0 to 50 on_resonance => 100 files, 2.7GB, 20M candidates
#   Keep 1% of the background makes a nice training set [=> training set]
# - Belle exp 55 run 0 to 20 on_resonance => 16 files, 78MB, 533K candidates, signal ~ 1%
# - Belle exp 55 run 0 to 30 on_resonance => 40 files, 
#  For real data use exp 55 run 0-30
# Note for release-04-01-01
# =========================
# - `dr` for tracks is calcualted correctly using passiveMoveBy
# - 
import basf2 as b2
import modularAnalysis as ma
import vertex as vtx
import b2biiConversion as b2c
import b2biiMonitors as b2m
import glob
import sys
import b2utils

from variables import variables as va
from variables.utils import create_aliases_for_selected

import argparse

if __name__ == '__main__':
    b2utils.print_b2env()
    
    isMC = True
    use_mva = False
    isTrain = True
    
    bkg_frac = 0.01

    infile = sys.argv[1]
    outfile = sys.argv[2]
    
    print(f"Input = {infile}")
    print(f"Output = {outfile}")
    
    mp = b2.create_path()
    b2c.convertBelleMdstToBelleIIMdst(infile, path = mp)
    
    va.addAlias('cosa', 'cosAngleBetweenMomentumAndVertexVector')
    va.addAlias('cosaXY', 'cosAngleBetweenMomentumAndVertexVectorInXYPlane')
    va.addAlias('abs_dM', 'abs(dM)')
    va.addAlias('abs_dr', 'abs(dr)')
    va.addAlias('min_dr', 'min(daughter(0, dr), daughter(1, dr))')
    va.addAlias('min_dz', 'min(daughter(0, dz), daughter(1, dz))')
    va.addAlias('pid_ppi', 'atcPIDBelle(4,2)')
    va.addAlias('pid_pk', 'atcPIDBelle(4,3)')
    va.addAlias('pid_kpi', 'atcPIDBelle(3,2)')
    va.addAlias('d0_PDG', 'daughter(0, mcPDG)')
    va.addAlias('d1_PDG', 'daughter(1, mcPDG)')
    va.addAlias('d2_PDG', 'daughter(2, mcPDG)')
    
    vtx.treeFit('Lambda0:mdst', 0, path = mp)
    ma.matchMCTruth('Lambda0:mdst', path = mp)
    
    ntuple = ['M', 'p', 'chiProb', 'cosa', 'cosaXY', 'dr', 'dz', 'distance', 
              'significanceOfDistance', 'min_dr', 'min_dz', 'goodBelleLambda'] + \
              isMC * ['isSignal', 'genMotherPDG']
    ntuple += ['IPX', 'IPY', 'IPZ']
    ntuple += create_aliases_for_selected(['pid_ppi', 'pid_pk', 'pid_kpi', 'dr', 'dz', 'p'] + \
                                          isMC * ['isSignal', 'genMotherPDG'],
                                          'Lambda0 -> ^p+ ^pi-', prefix = ['p', 'pi'])
    if use_mva:
        mp.add_module('MVAExpert', listNames = ['Lambda0:mdst'], extraInfoName = 'mva', 
                      identifier = 'belle_mva_lambda_v1.xml')
        va.addAlias('mva', 'extraInfo(mva)')
        ntuple += ['mva']
    
    if not isTrain:
        ma.variablesToNtuple('Lambda0:mdst', ntuple, treename = 'lambda', filename = outfile, path = mp)
        # ma.summaryOfLists('Lambda0:mdst', path = mp)
    else:
        # Downsample the background to make signal:background ~ 1
        ma.cutAndCopyList('Lambda0:sig', 'Lambda0:mdst', 'isSignal == 1', path = mp)
        ma.cutAndCopyList('Lambda0:bkg', 'Lambda0:mdst', f'isSignal == 0 and random < {bkg_frac}', path = mp)
        ma.copyLists('Lambda0:train', ['Lambda0:sig', 'Lambda0:bkg'], path = mp)
        ma.variablesToNtuple('Lambda0:train', ntuple, treename = 'lambda', filename = outfile, path = mp)
    
#     if isMC:
#         ma.fillParticleListFromMC('Lambda0:gen', '', addDaughters = True, path = mp)
# #         ma.matchMCTruth('Lambda0:gen', path = mp)
#         ma.variablesToNtuple('Lambda0:gen', ['M', 'cosa', 'd0_PDG', 'd1_PDG', 'd2_PDG'], 
#                              treename = 'lambda_gen', filename = outfile, path = mp)
    
    b2.process(path = mp)
    print(b2.statistics)