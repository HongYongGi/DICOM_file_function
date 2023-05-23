"""
Log

* Written by HongYongGi / email : hyg4438@gmail.com

* Written date : 20230523

3D Medical Image Plot function

    
"""

import os, glob, shutil
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def forceAspect(ax,aspect=1):
    """
    plot 되는 화면 1대1 유지 함수
    """
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def plot_3d(array, axis,title):
    """
    3D Medical Image Plot function

    Args:
        array (array): 3D array
        axis (list): plot x, y, z axis slice number list
        title (str): plot title
    """
    
    
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle(title, fontsize=16)
    ax1 = fig.add_subplot(131)
    # ax1.set_title(str)
    ax1.imshow(array[:, :, axis[2]], cmap='gray')
    ax1.axis('off')
    ax2 = fig.add_subplot(132)
    ax2.imshow(np.rot90(array[:, axis[1], :]), cmap='gray')   
    ax2.axis('off')
    ax3 = fig.add_subplot(133)
    ax3.imshow(np.rot90(array[axis[0], :, :]), cmap='gray')
    ax3.axis('off')

    forceAspect(ax1,1)
    forceAspect(ax2,1)
    forceAspect(ax3,1)    
    