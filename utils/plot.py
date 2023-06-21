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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from ipywidgets import interact
from IPython.display import clear_output


def forceAspect(ax,aspect=1):
    """
    plot 되는 화면 1대1 유지 함수
    """
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def plot_3d(array, axis,title, projection_flag = False):
    """
    3D Medical Image Plot function

    Args:
        array (array): 3D array
        axis (list): plot x, y, z axis slice number list
        title (str): plot title
    """
    
    if projection_flag ==False:
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
    else:
            
        fig = plt.figure(figsize=(15, 15))
        fig.suptitle(title, fontsize=16)
        ax1 = fig.add_subplot(131)
        # ax1.set_title(str)
        ax1.imshow(np.sum(array,2), cmap='gray')
        ax1.axis('off')
        ax2 = fig.add_subplot(132)
        ax2.imshow(np.rot90(np.sum(array,1)), cmap='gray')   
        ax2.axis('off')
        ax3 = fig.add_subplot(133)
        ax3.imshow(np.rot90(np.sum(array,0)), cmap='gray')
        ax3.axis('off')

        forceAspect(ax1,1)
        forceAspect(ax2,1)
        forceAspect(ax3,1)          
    
###########################################################################################
def convert_window(array, window_center, window_width):
    """
    윈도우 레벨 조절 함수 

    Args:
        array (array): ct_data
        window_center (int): window center number
        window_width (int): window_width number
    """
    array = np.clip(array, window_center - window_width // 2, window_center + window_width // 2)
    return array
    


# @interact(x_idx=(0, int(dicom_array.shape[0]-1)), y_idx=(0, int(dicom_array.shape[1]-1)), z_idx=(0, int(dicom_array.shape[2]-1)))
# def view(x_idx, y_idx, z_idx):
#     plot_3d(dicom_array, [x_idx, y_idx,  z_idx],'')


    
    
    

def meshgridnd_like(in_img, rng_func=range):
    new_shape = list(in_img.shape)
    all_range = [rng_func(i_len) for i_len in new_shape]
    return tuple([x_arr.swapaxes(0, 1) for x_arr in np.meshgrid(*all_range)])


def get_quiver_plot(flow_field, ds_factor = 18):
    """
    Params:
    flow_field: deformation field in the form of np.array: e.g., (512,512,112,3)
    ds_factor = an integer indicating the sparsity of the arrows in the quiver plot
    """
    DS_FACTOR = ds_factor
    print(flow_field.shape)
    # flow = np.moveaxis(flow_field, 0, -1)
    flow = flow_field

    c_xx, c_yy, c_zz = [x.flatten()
                        for x in
                        meshgridnd_like(flow[::DS_FACTOR, ::DS_FACTOR, ::DS_FACTOR, 0])]

    get_flow = lambda i: flow[::DS_FACTOR, ::DS_FACTOR, ::DS_FACTOR, i].flatten()

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')

    ax.quiver(c_xx,
              c_yy,
              c_zz,
              get_flow(0),
              get_flow(1),
              get_flow(2),
              length=0.5,
              normalize=True)



def animate_3d(image, threshold=-300): 
    p = image
    verts, faces, normals, values = measure.marching_cubes(p, threshold)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5, 0.5, 1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)
    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()
