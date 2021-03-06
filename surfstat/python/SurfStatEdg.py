import sys
import numpy as np
from matlab_functions import colon

def py_SurfStatEdg(surf):
	"""Converts the triangles or lattices of a mesh to edges. 

	Args:
		surf (dict): = a dictionary with key 'tri' or 'lat'
	        surf['tri'] = (t x 3) numpy array of triangle indices, t:#triangles, or,
	        surf['lat'] = 3D numpy array of 1's and 0's (1:in, 0:out).
		
	Returns:
		edg (np.array): A e-by-2 numpy array containing the indices of the edges, where
  			e is the number of edges. 
	"""

	if 'tri' in surf:
		tri = np.sort(surf['tri'], axis=1)
		edg =  np.unique(np.concatenate((np.concatenate((tri[:,[0, 1]], \
		                 tri[:,[0, 2]])),  tri[:,[1, 2]] )) , axis=0) 
		
	elif 'lat' in surf:
		# See the comments of SurfStatResels for a full explanation.
		if surf['lat'].ndim == 2:
			surf['lat'] = np.expand_dims(surf['lat'],axis=2)
		
		I, J, K = np.shape(surf['lat'])
		IJ = I * J
	
		a = np.arange(1, int(I)+1, dtype='int')
		b = np.arange(1, int(J)+1, dtype='int')
		
		i, j = np.meshgrid(a,b)
		i = i.T.flatten('F') 
		j = j.T.flatten('F')
		
		n1 = (I-1) * (J-1) * 6 + (I-1) * 3 + (J-1) * 3 + 1
		n2 = (I-1) * (J-1) * 3 + (I-1) + (J-1)

		edg = np.zeros(((K-1) * n1 + n2, int(2)), dtype='int')

		for f in range(0,2):
			
			c1  = np.where((np.remainder((i+j), 2) == f) & (i < I) & (j < J))[0] 
			c2  = np.where((np.remainder((i+j), 2) == f) & (i > 1) & (j < J))[0]
			c11 = np.where((np.remainder((i+j), 2) == f) & (i == I) & (j < J))[0]
			c21 = np.where((np.remainder((i+j), 2) == f) & (i == I) & (j > 1))[0]
			c12 = np.where((np.remainder((i+j), 2) == f) & (i < I) & (j == J))[0]
			c22 = np.where((np.remainder((i+j), 2) == f) & (i > 1) & (j == J))[0]
			
			# bottom slice
			edg0 = np.block([[ c1, c1, c1, c2-1, c2-1, c2, c11, c21-I, c12, \
							c22-1 ], [ c1+1, c1+I, c1+1+I, c2, c2-1+I, c2-1+I, \
							c11+I, c21, c12+1, c22 ]]).T +1
			# between slices
			edg1 = np.block([[ c1, c1, c1, c11, c11, c12, c12], [c1+IJ, c1+1+IJ, \
							c1+I+IJ, c11+IJ, c11+I+IJ, c12+IJ, c12+1+IJ ]]).T +1
			
			edg2 = np.block([[c2-1, c2, c2-1+I, c21-I, c21, c22-1, c22], \
							[c2-1+IJ, c2-1+IJ, c2-1+IJ, c21-I+IJ, c21-I+IJ, \
							c22-1+IJ, c22-1+IJ]]).T +1
						
			if f:
				for k in colon(2, K-1, 2):
					edg[(k-1)*n1 + np.arange(0,n1), :]  = (np.block([[edg0], \
						[edg2], [edg1], [IJ, 2*IJ]]) + (k-1) *IJ) 
			
			else:
				for k in colon(1, K-1, 2):
					edg[(k-1)*n1 + np.arange(0,n1), :]  = (np.block([[edg0], \
						[edg1], [edg2], [IJ, 2*IJ]]) + (k-1) *IJ) 
										
			if np.remainder((K+1), 2) == f:
				# top slice
				edg[ (K-1)*n1 + np.arange(0,n2), :]  = \
					edg0[np.arange(0,n2),:] + (K-1) * IJ
				
		# index by voxels in the "lat"
		vid = np.array(np.multiply(np.cumsum(surf['lat'][:].T.flatten()), \
			surf['lat'][:].T.flatten()) , dtype='int')
		vid = vid.reshape(len(vid),1)
		
		# only inside the lat
		all_idx = np.all(np.block([[surf['lat'].T.flatten()[edg[:,0] -1]], \
			[surf['lat'].T.flatten()[edg[:,1] -1]]]).T, axis=1)

		edg = vid[edg[all_idx,:]-1].reshape(np.shape(edg[all_idx,:]-1))
		
	else:
		sys.exit('input "surf" must have "lat" or "tri" key !!!')

	edg = edg - 1
  
	return edg

