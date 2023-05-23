import os, glob, shutil
from tqdm import tqdm
import pathlib




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
