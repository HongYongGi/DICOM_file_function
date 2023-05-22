"""
* Log 

* Written by HongYongGi / email: hyg4438@gmail.com

* Written date : 20230522

# Description
    * Convert Medical Image format
    * Convert DICOM to NIFTI
    * Convert NIFTI to DICOM
    * Convert NIFTI to raw
    * Convert raw to NIFTI
    

"""


# Package import
import os, glob, shutil
import numpy as np
import dicom2nifti
import dicom2nifti.settings as settings
settings.disable_validate_slice_increment()
settings.disable_validate_siemens_slice_increment()
settings.disable_validate_siemens_slice_timing()
import nibabel as nib
import pydicom
from tqdm import tqdm
import ipywidgets as widgets
from datetime import date


# Utils function

def load_nii(path):
    """
    # Description
        * Load NIFTI file
        

    Args:
        path (str): NIFTI file path
        
    Return :
        nii (nibabel.nifti1.Nifti1Image): NIFTI file
        affine (numpy.ndarray): affine matrix
        header (dict): header information
    
    """
    
    nii = nib.load(path)
    affine = nii.affine
    header = nii.header
    nii = nii.get_fdata()
    return nii, affine, header

def load_dcm(dicom_dir, information_flag = False):
    """
    
    # Description
        * Load DICOM file

    Args:
        dicom_dir (str): DICOM directory path
        
    Return :
        
    """
    
    
def nii2niigz(nii_path) : 
    """
    # Description
        * Convert NIFTI file to NIFTI GZ file

    Args:
        nii_path (str): NIFTI file path
        
    Returns:
        niigz_path (str): NIFTI GZ file path
    
    """
    
    nii = nib.load(nii_path)
    affine = nii.affine
    header = nii.header
    nii = nii.get_fdata()
    nii_image = nib.Nifti1Image(nii, affine, header)
    save_path = nii_path+ '.gz' 
    nib.save(nii_image, save_path)
    return save_path



def niigz2nii(niigz_path):
    """
    # Description
        * Convert NIFTI GZ file to NIFTI file
        

    Args:
        niigz_path (str): NIFTI GZ file path
    Returns:
        nii_path (str): NIFTI file path

    """

    nii = nib.load(niigz_path)
    affine = nii.affine
    header = nii.header
    nii = nii.get_fdata()
    nii_image = nib.Nifti1Image(nii, affine, header)
    save_path = niigz_path[:-3]
    nib.save(nii_image, save_path)
    return save_path



    
    