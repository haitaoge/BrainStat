import sys
sys.path.append("python")
from SurfStatResels import py_SurfStatResels
from SurfStatEdg import py_SurfStatEdg
import surfstat_wrap as sw
import numpy as np
import math
import itertools
import pytest
from scipy.io import loadmat

sw.matlab_init_surfstat()

def dummy_test(slm, mask=None):

    # Run MATLAB
    try:
        mat_output = sw.matlab_SurfStatResels(slm,mask)
        # Deal with either 1 or 3 output arguments.
        #if not isinstance(mat_output, np.ndarray):
        #    mat_output = mat_output[0].tolist()
        #    mat_output[1] = np.squeeze(mat_output[1])
        #else:
        mat_output = mat_output.tolist()
        if isinstance(mat_output,float):
            mat_output = [mat_output]
    except:
        pytest.skip("Original MATLAB code does not work with these inputs.")

    # Run Python
    resels_py,  reselspvert_py,  edg_py =  py_SurfStatResels(slm,mask)
    if len(mat_output) == 1:
        py_output = [resels_py]
    else:
        py_output = [resels_py,
                     reselspvert_py,
                     edg_py+1]
    
    # compare matlab-python outputs
    test_out = [] 
    for py, mat in zip(py_output,mat_output):
        result = np.allclose(np.squeeze(py),
                            np.squeeze(np.asarray(mat)),
                            rtol=1e-05, equal_nan=True)
        test_out.append(result)
    
    assert all(flag == True for (flag) in test_out)

# Test with only slm.tri
def test_01():
    slm = {'tri': np.array(
                  [[1,2,3],
                   [2,3,4], 
                   [1,2,4],
                   [2,3,5]])}
    dummy_test(slm)

# Test with slm.tri and slm.resl
def test_02():
    slm = {'tri': np.array(
               [[1,2,3],
                [2,3,4], 
                [1,2,4],
                [2,3,5]]),
          'resl': np.random.rand(8,6)}
    dummy_test(slm)

# Test with slm.tri, slm.resl, and mask
def test_03():
    slm = {'tri': np.array(
               [[1,2,3],
                [2,3,4], 
                [1,2,4],
                [2,3,5]]),
       'resl': np.random.rand(8,6)}
    mask = np.array([True,True,True,False,True])
    dummy_test(slm,mask)

# Test with slm.lat, 1's only.
def test_04():
    slm = {'lat': np.ones((10,10,10))}
    dummy_test(slm)

# Test with slm.lat, both 0's and 1's. 
def test_05():
    slm = {'lat': np.random.rand(10,10,10) > 0.5}
    dummy_test(slm)

# Test with slm.lat, both 0's and 1's, and a mask.
def test_06():
    slm = {'lat': np.random.rand(10,10,10) > 0.5}
    mask = np.random.choice([False,True],np.sum(slm['lat']))
    dummy_test(slm,mask)

# Test with slm.lat and slm.resl
def test_07():
    slm = {'lat': np.random.rand(10,10,10) > 0.5}
    edg = py_SurfStatEdg(slm)
    slm['resl'] = np.random.rand(edg.shape[0],1)
    dummy_test(slm)

# Test with slm.lat, slm.resl, and a mask
def test_08():
    slm = {'lat': np.random.rand(10,10,10) > 0.5}
    mask = np.random.choice([False,True],np.sum(slm['lat']))
    edg = py_SurfStatEdg(slm)
    slm['resl'] = np.random.rand(edg.shape[0],1)
    dummy_test(slm, mask) 

# Test with slm.lat, slm.resl, and a fully false mask
def test_09():
    slm = {'lat': np.random.rand(10,10,10) > 0.5}
    mask = np.zeros(np.sum(slm['lat']), dtype=bool)
    edg = py_SurfStatEdg(slm)
    slm['resl'] = np.random.rand(edg.shape[0],1)
    dummy_test(slm, mask) 
    
def test_10(): 
    slmfile = './tests/data/slm.mat'
    slmdata = loadmat(slmfile)
    slm = {}
    slm['tri'] = slmdata['slm']['tri'][0,0]    
    slm['resl'] = slmdata['slm']['resl'][0,0]
    dummy_test(slm)
    
# real data & random mask
def test_11():    
    slmfile = './tests/data/slm.mat'
    slmdata = loadmat(slmfile)
    slm = {}
    slm['tri'] = slmdata['slm']['tri'][0,0]    
    slm['resl'] = slmdata['slm']['resl'][0,0]
    # v is number of vertices
    v = slm['tri'].max()
    mask = np.random.choice([False,True], v)
    dummy_test(slm, mask)

# randomized (shuffled) real data    
def test_12():    
    slmfile = './tests/data/slm.mat'
    slmdata = loadmat(slmfile)
    slm = {}
    slm['tri'] = slmdata['slm']['tri'][0,0]    
    slm['resl'] = slmdata['slm']['resl'][0,0]
    np.random.shuffle(slm['tri'])
    np.random.shuffle(slm['resl'])
    dummy_test(slm)

# randomized (shuffled) real data & random mask
def test_13():    
    slmfile = './tests/data/slm.mat'
    slmdata = loadmat(slmfile)
    slm = {}
    slm['tri'] = slmdata['slm']['tri'][0,0]    
    slm['resl'] = slmdata['slm']['resl'][0,0]
    np.random.shuffle(slm['tri'])
    np.random.shuffle(slm['resl'])
    # v is number of vertices
    v = slm['tri'].max()
    mask = np.random.choice([False,True], v)
    dummy_test(slm, mask)    

