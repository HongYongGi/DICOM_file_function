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
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)  
import dicom2nifti
import dicom2nifti.settings as settings
settings.disable_validate_slice_increment()
import nibabel as nib
import pydicom
from pydicom import read_file

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
    nii = np.swapaxes(nii,0,1)
    return nii, affine, header

def save_nii(array, save_path, header = None , affine = np.eye(4)):
    
    """
    # Description
        * Save NIFTI file, header, affine is original information of NIFTI file
    
    Args: 
        array (numpy.ndarray): NIFTI array
        save_path (str): save path
        header (dict): header information
        affine (numpy.ndarray): affine matrix
        
    Returns : 
        save_path (str): save path
                
    """
    if header is None:
        nib.save(nib.Nifti1Image(array, affine), save_path)
    else : 
        nib.save(nib.Nifti1Image(array, affine, header), save_path)
    
    


def load_dcm(dicom_dir, information_flag = False):
    """
    
    # Description
        * Load DICOM file

    Args:
        dicom_dir (str): DICOM directory path
        information_flag (bool): If True, return information of DICOM file
        
    Return :
        if information_flag is True:
            dicom array, SeriesDescription, SliceThickness, PixelSpacing
        
        information_flag is False:
            dicom array
        
    """
    
    
    dicom_files = glob.glob(dicom_dir + '/*')
    if len(dicom_files) == 0 : 
        dicom_files = glob.glob(dicom_dir + '/*.DCM')
    elif len(dicom_files) == 0 : 
        dicom_files = glob.glob(dicom_dir + '/*')
    else:
        pass
    
    dicom_files.sort()
    
    dicoms = [read_file(dicom_file,force=True) for dicom_file in dicom_files]
    
    # 보통은 파일명으로 정렬되어 있지만, 그렇지 않은 경우가 있어서 정렬
    # sort dicoms by slices
    try: 
        slice_sorts = np.argsort([dicom.SliceLocation for dicom in dicoms])
        dicoms = [dicoms[slice_sort] for slice_sort in slice_sorts]    
    except:
        pass
    

    
    
    try :
        RescaleSlope = dicoms[0].RescaleSlope
        RescaleIntercept = dicoms[0].RescaleIntercept
    except: 
        RescaleSlope = 1
        RescaleIntercept = 0
    try: 
    
        image  = np.array([dicom.pixel_array * RescaleSlope + RescaleIntercept for dicom in dicoms])
        image  = np.transpose(image, axes=(1,2,0))
        
        
        
        slope = np.float32(dicoms[1].ImagePositionPatient[2]) - \
                np.float32(dicoms[0].ImagePositionPatient[2])
        orientation = np.float32(dicoms[0].ImageOrientationPatient[4])    
        
        
        if slope < 0:
            image = np.flip(image, -1)  # enforce feet first axially
            flipflag = 1
        if orientation < 0:
            image = np.flip(image, 0)  # enforce supine orientation
            flipflag = 2
            
        if (slope >= 0) and (orientation >= 0):
            flipflag = 3

        
        if information_flag==True : 
            Seriesdesc   = dicoms[0].SeriesDescription
            thickness    = dicoms[0].SliceThickness
            spacing      = dicoms[0].PixelSpacing   
                    
            
            return image, flipflag, Seriesdesc, thickness, spacing
        else: 
            return image, flipflag
    
    
    except: 
        print("Fail to load dicom directory : ", dicom_dir)
        flipflag =0
        return 0, flipflag

    
def dcm2nii(ref_dicom_dir, save_nii_dir, file_name, volume, flip_flag = 1):
    """
    
    # Description
        * Convert DICOM to NIFTI file
        
    Args:
        ref_dicom_dir (str): Target convert DICOM directory
        save_nii_dir (str): Save NIFTI directory 
        file_name (file name ): Save NIFTI file name(nii or nii.gz format)
        volume (array): 3D CT array
        flip_flag : 1-normal 2-slope flip 3-orientation flip
        
    Returns : 
        save_array : _description_
        
    example :
        >>> array = np.zeros((512,512,512))
        >>> ref_dicom_dir = 'C:/Users/.../dicom/'
        >>> save_nii_dir = 'C:/Users/.../nii/'
        >>> file_name = 'test.nii'
        >>> dcm2nii(ref_dicom_dir, save_nii_dir, file_name, volume)
    
    """    
    try: 
        os.makedirs(save_nii_dir)
    except:
        pass
    
    dicom2nifti.dicom_series_to_nifti(ref_dicom_dir, 
                                      save_nii_dir + 'temp.nii', 
                                      reorient_nifti=False)
    temp   = nib.load(save_nii_dir + 'temp.nii')
    header = temp.header
    affine = temp.affine
    
    
    if flip_flag == 1:
        save_format = np.transpose(volume, (1,0,2))
    elif flip_flag == 3:
        save_format = np.flip(np.transpose(volume, (1,0,2)), 2)
    else:
        save_format =np.flip(np.flip(np.transpose(volume, (1,0,2)), 0),1)
        
    
    save_nii_image = nib.Nifti1Image(save_format, affine, header)
    nib.save(save_nii_image, save_nii_dir + '/' + file_name)
    os.remove(save_nii_dir + 'temp.nii')    






    






# def dcm2niigz
# def nii2dcm
# def niigz2dcm
# def nii2raw
# def raw2nii
# def niigz2raw
# def raw2niigz
# def dcm2raw
# def raw2dcm

    
    
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

    
    
