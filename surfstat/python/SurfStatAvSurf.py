import numpy as np
import sys
import matlab.engine
import matlab
sys.path.append("matlab")

surfstat_eng = matlab.engine.start_matlab()
addpath = surfstat_eng.addpath("matlab")

def py_SurfStatAvSurf(filenames, fun='plus'):
    
    n, k = np.shape(filenames)
    n10 = int(np.floor(n/10))
    ab = 'a'
    
    for i in range(1, n+1):

        if np.remainder(np.float64(i), np.float64(n10)) == 0:
            print("NOT YET IMPLEMENTED")
            sys.exit()
        
        if i == 1:
            # THIS HAS TO BE CHANCED WITH BRAINSPACE EQUIVALENT
            s_mat, ab_mat  = surfstat_eng.SurfStatReadSurf(filenames[i-1],
                                                           ab , 2, nargout=2)
            s = {}
            s['tri'] = np.array(s_mat['tri'])       
            s['coord'] = np.array(s_mat['coord'])
            
            surf = {}
            surf['tri'] = s['tri']
            surf['coord'] = s['coord']
            
            m = 1
        else :
            print("NOT YET IMPLEMENTED")
            sys.exit()

        surf['coord'] = surf['coord'] / m
            
        return surf
            
            
            
# filenames are given as nested lists
filenames = [['/data/p_02323/hippocampus/data/shellsMni/HCP_996782_R_SUB.obj',
             '/data/p_02323/hippocampus/data/shellsMni/HCP_996782_L_SUB.obj']]

py_SurfStatAvSurf(filenames)