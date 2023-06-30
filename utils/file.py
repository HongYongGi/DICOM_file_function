import os, glob, shutil
from tqdm import tqdm
import pathlib
import pydicom
from pydicom import read_file



def search_files(root_dir):
    """
    root_dir: 검색을 시작할 디렉토리의 경로
    """
    for root, _, files in os.walk(root_dir):
        for file in files:
            yield os.path.join(root, file)
            
def search(root_dir):
    """
    root_dir: 검색을 시작할 디렉토리의 경로

    Args:
        root_dir (str): 검색할 디렉토리
    Returns:
        file_list (list) : 검색된 파일의 경로 리스트
        
    """
    file_list = []
    for file_path in search_files(root_dir):
        file_list.append(file_path)
    return file_list

def split_path (path) :
    """
    Split path
    * Split path

    Args:
        path (str): path
        
    Return 
        split path
    
    
    """
    split_path = path.split('\\')
    return split_path


def Anonymized_header(dicom_path):
    header_info = read_file(dicom_path)
    
    tags_to_remove = [
        0x00100020,  # Patient ID
        0x00200010,  # Study ID
        0x00080080,  # Institution Name
        0x00080081,  # Institution Address
        0x00080090,  # Referring Physician's Name
        0x00081040,  # Institutional Department Name
        0x00081050,  # Performing Physician's Name
        0x00081070,  # Operator's Name
        0x00100010,  # Patient's Name
        0x00100030,  # Patient's Birth Date
        0x00100040,  # Patient Sex
        0x00101010,  # Patient's Age
        0x00080020,  # Study Date
        0x00080021,  # Series Date
        0x00080022,  # Acquisition Date
        0x00080023,  # Content Date
        0x00080030,  # Study Time
        0x00080031,  # Series Time
        0x00080032,  # Acquisition Time
        0x00080033,  # Content Time
        0x00080050,  # Accession Number
        0x00081032,  # Procedure Code Sequence
        0x00080100,  # Code Value
        0x00080102,  # Coding Scheme Designator
        0x00080104,  # Code Meaning
        0x00081030,  # Study Description
        0x0008103E,  # Series Description
        0x00081040,  # Institutional Department Name
        0x00180015,  # Body Part Examined
        0x00180024,  # Sequence Name
        0x00180030,  # Protocol Name
        0x00400244,  # Performed Procedure Step Start Date
        0x00400245,  # Performed Procedure Step Start Time
        0x00400253,  # Performed Procedure Step ID
        0x00400254,  # Performed Procedure Step Description
        0x00400007,  # Scheduled Procedure Step Description
        0x00400009,  # Scheduled Procedure Step ID
        0x00401001,  # Requested Procedure ID
        0x00204000,  # Image Comments
        0x00321060,  # Requested Procedure Description
        0x00321032   # Requesting Physician
    ]
    for tag in tags_to_remove:
        try:
            del header_info[tag]
        except:
            pass

    header_info.save_as(dicom_path)