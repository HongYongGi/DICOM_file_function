# DICOM_file_function


DICOM & Nifti file util function

* Convert format function

* 3D plot function


***Medical Image format (dcm, nii, nii.gz, raw)***



---

### Usage

```
os.sys.path.append('./DICOM_file_function/')
from utils import *
```

### 1. Convert format function

* Convert DICOM to Nifti

```
dicom2nifti(dicom_path, nifti_path)
```

* Convert Nifti to DICOM

```
nifti2dicom(nifti_path, dicom_path)
```

* Convert Nifti to Nifti.gz

```
nifti2nifti_gz(nifti_path, nifti_gz_path)
```

* Convert Nifti.gz to Nifti

```
nifti_gz2nifti(nifti_gz_path, nifti_path)
```

* Convert Nifti to Raw

```
nifti2raw(nifti_path, raw_path)
```

* Convert Raw to Nifti

```
raw2nifti(raw_path, nifti_path)
```



## 2. Load file

* Load DICOM file

```
dicom = load_dcm(dicom_path)
```

* Load Nifti file

```
nifti = load_nii(nifti_path)
```






