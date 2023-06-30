


## Lung Lesion related functions


def split_into_instance(segmentation_mask_array):
    binary_mask = (segmentation_mask > 0).astype(np.uint8)
    
    
    
    # 인스턴스 레이블링
    labeled_mask, num_instances = label(binary_mask,background=0, connectivity=1, return_num=True)
    print(np.unique(labeled_mask))
    print(num_instances)
    return labeled_mask



