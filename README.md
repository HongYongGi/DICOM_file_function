# DICOM_file_function

Medical image processing and analysis utilities for DICOM & NIFTI files.

## Features

* **Format Conversion**: Convert between DICOM, NIFTI, NIFTI.GZ, and RAW formats
* **3D Visualization**: Interactive 3D plotting and animation functions
* **Evaluation Metrics**: Comprehensive medical image analysis metrics
* **File Operations**: File search, anonymization, and utility functions
* **Image Registration**: Affine registration and transformation tools
* **RECIST Analysis**: Lung lesion analysis and measurement tools

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DICOM_file_function
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Quick Start

```python
import sys
sys.path.append('./DICOM_file_function/')
from utils import *

# Load DICOM file
dicom_image, flipflag, Seriesdesc, thickness, spacing = load_dcm(dicom_path, information_flag=True)

# Load NIFTI file
nii, affine, header = load_nii(nifti_path)

# Convert DICOM to NIFTI
dcm2nii(ref_dicom_dir, save_nii_dir, file_name, volume, flip_flag)

# 3D visualization
plot_3d(array, axis, title='3D Plot', projection_flag=False)
```

## Detailed Usage Guide

### 1. File Loading

#### Load DICOM file
```python
# Basic loading
dicom_image, flipflag = load_dcm(dicom_path, information_flag=False)

# With detailed information
dicom_image, flipflag, Seriesdesc, thickness, spacing = load_dcm(dicom_path, information_flag=True)
```

**Parameters:**
- `dicom_path` (str): Path to DICOM directory containing multiple DICOM files
- `information_flag` (bool): If True, returns additional metadata

**Returns:**
- `dicom_image` (numpy.ndarray): 3D volume array (height, width, slices)
- `flipflag` (int): Orientation flag for proper NIFTI conversion
  - 1: Normal orientation
  - 2: Supine orientation flip needed
  - 3: Feet-first axial flip needed
- `Seriesdesc` (str): Series description (only if information_flag=True)
- `thickness` (float): Slice thickness in mm (only if information_flag=True)
- `spacing` (list): Pixel spacing [x, y] in mm (only if information_flag=True)

**Example:**
```python
# Load CT scan with metadata
ct_volume, flip_flag, series_desc, slice_thickness, pixel_spacing = load_dcm(
    "path/to/ct_scan_folder/", 
    information_flag=True
)
print(f"Series: {series_desc}")
print(f"Slice thickness: {slice_thickness}mm")
print(f"Pixel spacing: {pixel_spacing}mm")
```

#### Load NIFTI file
```python
nii, affine, header = load_nii(nifti_path)
```

**Parameters:**
- `nifti_path` (str): Path to NIFTI file (.nii or .nii.gz)

**Returns:**
- `nii` (numpy.ndarray): 3D volume array (height, width, slices)
- `affine` (numpy.ndarray): 4x4 affine transformation matrix
- `header` (dict): NIFTI header information

**Example:**
```python
# Load NIFTI file
volume, affine_matrix, header_info = load_nii("path/to/image.nii.gz")
print(f"Volume shape: {volume.shape}")
print(f"Voxel size: {header_info.get_zooms()}")
```

### 2. Format Conversion

#### DICOM to NIFTI
```python
dcm2nii(ref_dicom_dir, save_nii_dir, file_name, volume, flip_flag)
```

**Parameters:**
- `ref_dicom_dir` (str): Reference DICOM directory for header information
- `save_nii_dir` (str): Directory to save NIFTI file
- `file_name` (str): Output NIFTI filename (e.g., "output.nii" or "output.nii.gz")
- `volume` (numpy.ndarray): 3D volume array to save
- `flip_flag` (int): Orientation flag from load_dcm function

**Example:**
```python
# Convert DICOM to NIFTI
dcm2nii(
    ref_dicom_dir="path/to/original_dicom/",
    save_nii_dir="path/to/output/",
    file_name="converted_scan.nii.gz",
    volume=ct_volume,
    flip_flag=flip_flag
)
```

#### NIFTI to NIFTI.GZ (compressed)
```python
compressed_path = nii2niigz(nifti_path)
```

**Parameters:**
- `nifti_path` (str): Path to uncompressed NIFTI file

**Returns:**
- `compressed_path` (str): Path to compressed NIFTI file

**Example:**
```python
# Compress NIFTI file
compressed_file = nii2niigz("large_volume.nii")
print(f"Compressed file: {compressed_file}")
```

#### NIFTI.GZ to NIFTI (decompress)
```python
decompressed_path = niigz2nii(nifti_gz_path)
```

**Parameters:**
- `nifti_gz_path` (str): Path to compressed NIFTI file

**Returns:**
- `decompressed_path` (str): Path to uncompressed NIFTI file

**Example:**
```python
# Decompress NIFTI file
decompressed_file = niigz2nii("compressed_volume.nii.gz")
print(f"Decompressed file: {decompressed_file}")
```

### 3. 3D Visualization

#### 3D Plot
```python
plot_3d(array, axis, title='', projection_flag=False, 
        sub1_title='', sub2_title='', sub3_title='')
```

**Parameters:**
- `array` (numpy.ndarray): 3D volume array
- `axis` (int): Plot axis (0, 1, or 2)
- `title` (str): Main plot title
- `projection_flag` (bool): If True, shows projection plots instead of 3D
- `sub1_title`, `sub2_title`, `sub3_title` (str): Subplot titles

**Example:**
```python
# 3D volume plot
plot_3d(
    array=ct_volume,
    axis=2,  # Axial view
    title="CT Scan - Axial View",
    projection_flag=False
)

# 3D projection plot
plot_3d(
    array=ct_volume,
    axis=2,
    title="CT Scan - Projection View",
    projection_flag=True,
    sub1_title="Sagittal",
    sub2_title="Coronal", 
    sub3_title="Axial"
)
```

#### 3D Animation
```python
animate_3d(image, threshold=-300)
```

**Parameters:**
- `image` (numpy.ndarray): 3D volume array
- `threshold` (float): Threshold value for surface rendering

**Example:**
```python
# Create 3D animation
animate_3d(ct_volume, threshold=-300)
```

### 4. Evaluation Metrics

#### Confusion Matrix and Metrics
```python
# Get all metrics at once
dice, sensitivity, precision, recall, f1_score, fpr = confusion_matrix(label, predict)

# Get confusion matrix components
tp, fp, fn, tn = confusion_matrix(label, predict, cm_flag=True)
```

#### Individual Metrics
```python
# Dice coefficient
dice_score = dice(label, predict)

# Sensitivity (True Positive Rate)
sensitivity_score = sensitivity(label, predict)

# Precision (Positive Predictive Value)
precision_score = precision(label, predict)

# Recall (True Positive Rate)
recall_score = recall(label, predict)

# F1 Score
f1_score_val = f1_score(label, predict)

# False Positive Rate
fpr_score = fpr(label, predict)
```

#### Image Quality Metrics
```python
# Structural Similarity Index
ssim_score = ssim(label, predict)

# Peak Signal-to-Noise Ratio
psnr_score = psnr(label, predict)

# Mean Absolute Error
mae_score = mae(label, predict)

# Mean Squared Error
mse_score = mse(label, predict)

# Root Mean Squared Error
rmse_score = rmse(label, predict)
```

**Example:**
```python
# Evaluate segmentation results
ground_truth = load_nii("ground_truth.nii.gz")[0]
prediction = load_nii("prediction.nii.gz")[0]

# Calculate all metrics
dice, sens, prec, rec, f1, fpr = confusion_matrix(ground_truth, prediction)
print(f"Dice: {dice:.3f}")
print(f"Sensitivity: {sens:.3f}")
print(f"Precision: {prec:.3f}")

# Calculate image quality
ssim_val = ssim(ground_truth, prediction)
psnr_val = psnr(ground_truth, prediction)
print(f"SSIM: {ssim_val:.3f}")
print(f"PSNR: {psnr_val:.3f}")
```

### 5. File Operations

#### Search Files
```python
# Search all files in directory
file_list = search(root_dir)

# Generator for large directories
for file_path in search_files(root_dir):
    print(file_path)
```

**Parameters:**
- `root_dir` (str): Directory to search

**Returns:**
- `file_list` (list): List of file paths

#### Anonymize DICOM Header
```python
Anonymized_header(dicom_path)
```

**Parameters:**
- `dicom_path` (str): Path to DICOM file

**Example:**
```python
# Anonymize patient information
Anonymized_header("patient_scan.dcm")
```

#### Split Path
```python
path_components = split_path(path)
```

**Parameters:**
- `path` (str): File path to split

**Returns:**
- `path_components` (list): List of path components

**Example:**
```python
# Split Windows path
components = split_path("C:\\Users\\User\\Documents\\file.txt")
print(components)  # ['C:', 'Users', 'User', 'Documents', 'file.txt']
```

### 6. Image Registration

#### Preprocess Image
```python
processed_image = preprocess(image)
```

**Parameters:**
- `image` (numpy.ndarray): Input image

**Returns:**
- `processed_image` (numpy.ndarray): Preprocessed image

#### Affine Registration
```python
registered_image = affine_registration(fixed_image, moving_image)
```

**Parameters:**
- `fixed_image` (numpy.ndarray): Reference image
- `moving_image` (numpy.ndarray): Image to be registered

**Returns:**
- `registered_image` (numpy.ndarray): Registered image

#### Affine Transform
```python
transformed_image = affine_transform(image, transform_matrix)
```

**Parameters:**
- `image` (numpy.ndarray): Input image
- `transform_matrix` (numpy.ndarray): Transformation matrix

**Returns:**
- `transformed_image` (numpy.ndarray): Transformed image

**Example:**
```python
# Register two images
fixed_img = load_nii("fixed.nii.gz")[0]
moving_img = load_nii("moving.nii.gz")[0]

# Preprocess images
fixed_processed = preprocess(fixed_img)
moving_processed = preprocess(moving_img)

# Perform registration
registered_img = affine_registration(fixed_processed, moving_processed)
```

### 7. RECIST Analysis

#### Lung Lesion Analysis
```python
# Clip lung region
lung_region = Lung_clip(image)

# Split into individual lesions
lesion_instances = split_into_instances(segmentation_mask)

# Calculate volume
volume = calculate_volume(mask)

# Find lesion mask
lesion_mask = find_instance_mask(image)

# Calculate distance between points
distance = calculate_distance(point1, point2)

# Find closest coordinates
closest_point = find_closest_coordinates(target_point, coordinate_list)

# Select target lesions
fixed_lesion = select_target_lesion_fixed(image)
moved_lesion = select_target_lesion_moved(image)
moving_lesion = select_target_lesion_moving(image)

# Calculate diameter
diameter = calculate_diameter(lesion_mask)

# Get lesion information
info = get_information(lesion_data)
```

**Example:**
```python
# Analyze lung lesions
ct_scan = load_nii("lung_scan.nii.gz")[0]

# Clip lung region
lung_clipped = Lung_clip(ct_scan)

# Find individual lesions
lesions = split_into_instances(segmentation_mask)

# Calculate volumes
for i, lesion in enumerate(lesions):
    volume = calculate_volume(lesion)
    diameter = calculate_diameter(lesion)
    print(f"Lesion {i}: Volume={volume:.2f}mm³, Diameter={diameter:.2f}mm")
```

### 8. Utility Functions

#### Normalize Array
```python
normalized_array = norm(array)
```

**Parameters:**
- `array` (numpy.ndarray): Input array

**Returns:**
- `normalized_array` (numpy.ndarray): Normalized array (0-1 range)

**Example:**
```python
# Normalize CT values
normalized_ct = norm(ct_volume)
print(f"Range: {normalized_ct.min():.3f} - {normalized_ct.max():.3f}")
```

## Complete Example

```python
import sys
sys.path.append('./DICOM_file_function/')
from utils import *

# 1. Load DICOM data
dicom_path = "path/to/dicom_folder/"
ct_volume, flip_flag, series_desc, thickness, spacing = load_dcm(dicom_path, information_flag=True)

# 2. Convert to NIFTI
output_dir = "path/to/output/"
dcm2nii(dicom_path, output_dir, "converted_scan.nii.gz", ct_volume, flip_flag)

# 3. 3D visualization
plot_3d(ct_volume, axis=2, title="CT Scan", projection_flag=True)

# 4. Evaluate segmentation
ground_truth = load_nii("ground_truth.nii.gz")[0]
prediction = load_nii("prediction.nii.gz")[0]

dice_score = dice(ground_truth, prediction)
ssim_score = ssim(ground_truth, prediction)
print(f"Dice: {dice_score:.3f}, SSIM: {ssim_score:.3f}")

# 5. Lung lesion analysis
lung_region = Lung_clip(ct_volume)
lesions = split_into_instances(segmentation_mask)

for i, lesion in enumerate(lesions):
    volume = calculate_volume(lesion)
    print(f"Lesion {i} volume: {volume:.2f}mm³")
```

## Requirements

See `requirements.txt` for the complete list of dependencies.

### Core Dependencies
- numpy>=1.20.0
- pydicom>=2.3.0
- nibabel>=3.2.0
- dicom2nifti>=2.4.0
- matplotlib>=3.3.0
- scikit-image>=0.18.0

## Recent Updates

- Fixed compatibility issues with latest pydicom version
- Removed deprecated numpy warnings
- Cleaned up duplicate functions
- Added comprehensive requirements.txt
- Improved code organization and documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

* Written by HongYongGi / email: hyg4438@gmail.com
* Written date: 20230522