import numpy as np
import sys
import matlab.engine
import matlab
sys.path.append("matlab")

surfstat_eng = matlab.engine.start_matlab()
addpath = surfstat_eng.addpath("matlab")

def py_SurfStatAvSurf(filenames, fun = np.add):
    """Average, minimum or maximum of surfaces.

    Parameters
    ----------
    filenames : nested list of filenames, size (n,k)
        fileformats: ?????????????????????
    fun : function handle to operate on surfaces, e.g.
        np.add (default) will give the average of the surfaces, 
        np.min or np.max will give the min or max, respectively.
    Returns
    -------
    surf : dict
        Dictionary with the following keys:

        - 'coord' : ndarray, shape = (3,v)
            Average coordinates, v is the number of vertices.
        - 'tri' : ndarray, shape = (t,3)
            Triangle indices.
    """    
    
    n, k = np.shape(filenames)
    n10 = int(np.floor(n/10))
    ab = 'a'
    surf = {}
    
    for i in range(1, n+1):
            
        if i == 1:
            # THIS HAS TO BE CHANCED WITH BRAINSPACE EQUIVALENT
            s_mat, ab_mat  = surfstat_eng.SurfStatReadSurf(filenames[i-1],
                                                           ab, 2, nargout=2)
            s = {}
            s['tri'] = np.array(s_mat['tri'])       
            s['coord'] = np.array(s_mat['coord'])
            
            surf['tri'] = s['tri']
            surf['coord'] = s['coord']
            
            m = 1
        else :
            # THIS HAS TO BE CHANCED WITH BRAINSPACE EQUIVALENT
            s_mat, ab_mat  = surfstat_eng.SurfStatReadSurf(filenames[i-1],
                                                           ab, 1, nargout=2)
            s = {}     
            s['coord'] = np.array(s_mat['coord'])
            
            surf['coord'] = fun(surf['coord'], s['coord'])
            m = fun(m, 1) 

    surf['coord'] = surf['coord'] / m
    return surf
            
            
            
# filenames are given as nested lists
filenames = [['/data/p_02323/hippocampus/data/shellsMni/HCP_996782_R_SUB.obj',
             '/data/p_02323/hippocampus/data/shellsMni/HCP_996782_L_SUB.obj'],
             ['/data/p_02323/hippocampus/data/shellsMni/HCP_994273_R_SUB.obj',
              '/data/p_02323/hippocampus/data/shellsMni/HCP_994273_L_SUB.obj']]

py_SurfStatAvSurf(filenames, fun = np.min)
