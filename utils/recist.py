import numpy as np
from ants import from_numpy, resample_image, apply_transforms, registration
from skimage.measure import label




def Lung_clip(array, level= -500, window = 2000):
    max_value = level + window/2
    min_value = level - window/2
    # 500~ -1500
    lung_volume = np.clip(array, min_value, max_value, array)
    return lung_volume

def split_into_instances(segmentation_mask):
    # Segmentation 마스크 이진화
    binary_mask = (segmentation_mask > 0).astype(np.uint8)

    # 인스턴스 레이블링
    labeled_mask, num_instances = label(binary_mask,background=0, connectivity=3, return_num=True)
    # print(np.unique(labeled_mask))
    
    return labeled_mask


def calculate_volume(ct_mask):
    """
    This function is to calculate the volume of tumor.

    Args:
        ct_mask (numpy.ndarray): 3D array of tumor mask
    Returns:
        volume (dict): instance number and volume of tumor
    
    Exmaple)
    >>> dummy_mask  = np.zeros((512,512,59))
    >>> dummy_mask[100:200, 100:200, 20:40] = 1
    >>> dummy_mask[300:400, 300:400, 20:40] = 2
    >>> calculate_volume(dummy_mask)
    {1.0: 200000, 2.0: 200000}
    
    """
    instance, count  = np.unique(ct_mask, return_counts=True)
    return dict(zip(instance[1:], count[1:]))



def find_instance_mask(ct_mask):
    """
    This function is to find the instance center of tumor.
    
    Args:
        ct_mask (numpy.ndarray): 3D array of tumor mask
        
    Returns:
        centers (dict): instance number and center of tumor
        
    Example)
    >>> dummy_mask  = np.zeros((512,512,59))
    >>> dummy_mask[100:200, 100:200, 20:40] = 1
    >>> dummy_mask[300:400, 300:400, 20:40] = 2
    >>> find_instance_mask(dummy_mask)
    {1.0: [149.5, 149.5, 29.5], 2.0: [349.5, 349.5, 29.5]}
    
    """
    class_nums = np.unique(ct_mask)[1:] # 0을 제외해야 하기 때문에 1부터 시작
    centers = {}
    for class_num in class_nums:
        location  = np.where(ct_mask == class_num)
        x = np.round(np.mean(location[0]),3)
        y = np.round(np.mean(location[1]),3)
        z = np.round(np.mean(location[2]),3)
        centers[class_num] = [x,y,z]
    
    return centers


def calculate_distance(center1, center2):
    """
    This function is to calculate the distance between two centers.
    Args: 
        center1 (list): center1 
        center2 (list): center2
    Returns :
        distance (float): distance between two centers
        
    """
    
    return np.sqrt(np.sum(np.square(np.array(center1) - np.array(center2))))


def find_closest_coordinates(target_center, centers_list):
    """
    This code is to find the closest coordinates from target center.
    
    Args: 
        target_center (list): target center
        centers_list (list): list of centers
    Returns:
        closest_coordinates (list): closest coordinates
    
    """
    distance  = []
    for center in centers_list:
        distance.append(calculate_distance(target_center,centers_list[center]))
    index = distance.index(min(distance)) + 1
    
    return index , centers_list[index], min(distance)

    


def select_target_lesion_fixed(ct_mask, Target_lesion_numbers):
    """
    This function is to select the target lesion.

    Args:
        ct_mask (_type_): _description_
        Target_lesion_numbers (_type_): _description_
    Returns:
        target_lesion_mask (_type_): _description_
    """
    
    
    volume_dict   = calculate_volume(ct_mask)
    sorted_volume = sorted(volume_dict.items(), key=lambda x: x[1], reverse=True)
    select_volume = sorted_volume[:Target_lesion_numbers]
    not_select_volume = sorted_volume[Target_lesion_numbers:]
    not_select_mask= np.zeros((ct_mask.shape))
    select_mask    = np.zeros((ct_mask.shape))
    instance = 1
    for i in select_volume:
        select_mask[ct_mask == i[0]] = instance
        instance += 1
    n_instance  = 1
    for i in not_select_volume:
        not_select_mask[ct_mask == i[0]] = n_instance
        n_instance += 1
    
        
    return select_mask, not_select_mask


def select_target_lesion_moved(moved_ct_mask, fixed_ct_mask, non_target_fixed_ct_mask, Threshold_diameter  = 100):
    """
    This function is to select the target lesion.

    Args:
        moved_ct_mask (numpy.ndarray): Target CT mask
        fixed_ct_mask (numpy.ndarray): Fixed CT mask selected by select_target_lesion_fixed function
        
    Returns:
        target_lesion_mask (numpy.ndarray): Target lesion mask
    
    """
    moved_centers     = find_instance_mask(moved_ct_mask)
    fixed_centers     = find_instance_mask(fixed_ct_mask)
    
    new_ct_mask       = np.zeros((moved_ct_mask.shape))
    
    
    selected_ct_mask  = np.zeros((moved_ct_mask.shape))
    for f_center in fixed_centers:
        index, m_center, distance  = find_closest_coordinates(fixed_centers[f_center], moved_centers)
        
        if distance < Threshold_diameter:
            selected_ct_mask[moved_ct_mask  == index] = f_center
        elif distance >= Threshold_diameter:
            new_ct_mask[moved_ct_mask  == index] = f_center
        
        
    non_fixed_centers  = find_instance_mask(non_target_fixed_ct_mask)
    non_selected_ct_mask = np.zeros((moved_ct_mask.shape))   
    for nf_center in non_fixed_centers:
        index, m_center, distance  = find_closest_coordinates(non_fixed_centers[nf_center], moved_centers)
        if distance < Threshold_diameter:
            non_selected_ct_mask[moved_ct_mask  == index] = nf_center
        elif distance >= Threshold_diameter:
            new_ct_mask[moved_ct_mask  == index] = nf_center        
    
        
        
    return selected_ct_mask, non_selected_ct_mask, new_ct_mask
        
        
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
        
        
        
        
        
        
def select_target_lesion_moving(moving_ct_mask, 
                                moved_ct_mask,
                                non_moved_ct_mask ,
                                new_moved_ct_mask,
                                md_m_affine_matrix):
    """
    This function is to select the target lesion in the moving CT mask.

    Args:
        moving_ct_mask (numpy array): The moving CT mask.
        moved_ct_mask (numpy array): Moved CT mask selected by select_target_lesion_moved function
        
    retunrs: 
        target_lesion_mask(numpy array): Target lesion mask
    
    """
    
    # Target lesion
    affine_tumor_m  = np.zeros((moving_ct_mask.shape))
    class_nums = np.unique(moved_ct_mask)[1:] # 0을 제외해야 하기 때문에 1부터 시작

    for instance_id in class_nums : 
        tumor_moved  = moved_ct_mask.copy()
        tumor_moved[tumor_moved==instance_id]= instance_id
        tumor_moved[tumor_moved!=instance_id]= 0
        tumor_moved = tumor_moved.astype(np.uint8)
        temp_m = affine_transform(md_m_affine_matrix, tumor_moved, tumor_moved,0)
        temp_m = split_into_instances(temp_m)
        affine_tumor_m[temp_m == 1] = instance_id
        
    moving_centers         = find_instance_mask(moving_ct_mask)
    affine_moving_centers  = find_instance_mask(affine_tumor_m)
    select_lesion_ct_mask  = np.zeros((moving_ct_mask.shape))     
    
    for f_center in affine_moving_centers:
        index, m_center, distance  = find_closest_coordinates(affine_moving_centers[f_center], moving_centers)
        select_lesion_ct_mask[moving_ct_mask  == index] = f_center
        
        

    # Non-target lesion
    affine_tumor_m1 = np.zeros((moving_ct_mask.shape))
    class_nums = np.unique(non_moved_ct_mask)[1:] # 0을 제외해야 하기 때문에 1부터 시작
    for instance_id1 in class_nums : 
        tumor_moved1  = non_moved_ct_mask.copy()
        tumor_moved1[tumor_moved1==instance_id1]= instance_id1
        tumor_moved1[tumor_moved1!=instance_id1]= 0
        tumor_moved1 = tumor_moved1.astype(np.uint8)
        temp_m1 = affine_transform(md_m_affine_matrix, tumor_moved1, tumor_moved1,0)
        temp_m1 = split_into_instances(temp_m1)
        affine_tumor_m1[temp_m1 == 1] = instance_id1
    
    affine_moving_centers1    = find_instance_mask(affine_tumor_m1)
    non_select_lesion_ct_mask = np.zeros((moving_ct_mask.shape))
    for f_center1 in affine_moving_centers1:
        index1, m_center1, distance1  = find_closest_coordinates(affine_moving_centers1[f_center1], moving_centers)
        non_select_lesion_ct_mask[moving_ct_mask  == index1] = f_center1
    
    # New Lesion
    affine_tumor_m2 = np.zeros((moving_ct_mask.shape))
    class_nums = np.unique(new_moved_ct_mask)[1:] # 0을 제외해야 하기 때문에 1부터 시작
    for instance_id2 in class_nums:
        tumor_moved2  = new_moved_ct_mask.copy()
        tumor_moved2[tumor_moved2==instance_id2]= instance_id2
        tumor_moved2[tumor_moved2!=instance_id2]= 0
        tumor_moved2 = tumor_moved2.astype(np.uint8)
        temp_m2 = affine_transform(md_m_affine_matrix, tumor_moved2, tumor_moved2,0)
        temp_m2 = split_into_instances(temp_m2)
        affine_tumor_m2[temp_m2 == 1] = instance_id2
    affine_moving_centers2    = find_instance_mask(affine_tumor_m2)
    new_lesion_ct_mask = np.zeros((moving_ct_mask.shape))
    for f_center2 in affine_moving_centers2:
        index2, m_center2, distance2  = find_closest_coordinates(affine_moving_centers2[f_center2], moving_centers)
        new_lesion_ct_mask[moving_ct_mask  == index2] = f_center2    
        
        
        
    return select_lesion_ct_mask, non_select_lesion_ct_mask, new_lesion_ct_mask    

################
# RECIST utils #
################
def calculate_diameter(binary_mask, key_slice):
    location  =  np.where(binary_mask == 1)
    
    
    x,y,z = location[0], location[1], key_slice
    
    longest_diameter  = 0
    for idx in range(len(x)):
        for idx2 in  range(len(x)):
            diameter  = np.sqrt((x[idx] - x[idx2])**2 + (y[idx] - y[idx2])**2)
            if diameter > longest_diameter:
                longest_diameter = diameter
    return longest_diameter
    


def get_information(CT_mask): 
    num_class = np.unique(CT_mask)[1:]
    information = {}
    total_LD  = []
    for idx in num_class:
        mask = np.zeros((CT_mask.shape))
        mask[CT_mask == idx] = 1
        z_hist  = np.sum(mask, axis = (0,1))
        # print(z_hist)
        key_slice  = np.where(z_hist==max(z_hist))[0][0]
        LD         = calculate_diameter(mask, key_slice)
        LD         = np.round(LD, 3)
        total_LD.append(LD)
        information[idx] = [key_slice, LD]
    return information , np.sum(total_LD)   


