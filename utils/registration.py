import os, glob, shutil
import numpy as np
import nibabel as nib
from tqdm import tqdm
from ants import from_numpy, resample_image, apply_transforms, registration

def preprocess(arr, shape, interp = 4):
    """
    Resample CT data to target shape
    Using ANTsPy package
    

    Args:
        arr (arr): ct array
        shape (int): voxelmorph input shape 
        resample_method (int, optional):  Select Interpolation method
    """
    arr = from_numpy(arr)
    arr = resample_image(arr, shape,1, interp_type=interp)[:, :, :]
    return arr



def affine_registration(fixed, moving, a = 'AffineFast'):     # fixed (insp) moving (exp) for lung mask
    """ Affine registration of a moving image to a fixed image"""

    affine_reg = registration(fixed=from_numpy(fixed),
                              moving=from_numpy(moving),
                              type_of_transform=a)
    return affine_reg



def affine_transform(affine_reg, fix, move,defaultvalue_num= -1024, inverse_flag = False):
    """ Affine registration of expiratory image and lung masks to
        inspiratory image
        
        
    interpolator : string
        Choice of interpolator. Supports partial matching.
            linear
            nearestNeighbor
            multiLabel for label images (deprecated, prefer genericLabel)
            gaussian
            bSpline
            cosineWindowedSinc
            welchWindowedSinc
            hammingWindowedSinc
            lanczosWindowedSinc
            genericLabel use this for label images        
        
    """
    # affine register image
    if inverse_flag==False:
            
        exp_affine = apply_transforms(fixed=from_numpy(fix),
                                    moving=from_numpy(move),
                                    transformlist=affine_reg['fwdtransforms'],
                                    
                                    defaultvalue = defaultvalue_num
                                    )[:, :, :]
    else:
        exp_affine = apply_transforms(fixed=from_numpy(fix),
                                    moving=from_numpy(move),
                                    transformlist=affine_reg['invtransforms'],
                                    
                                    defaultvalue = defaultvalue_num
                                    )[:, :, :]
        

    return exp_affine
