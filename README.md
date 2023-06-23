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


---

## 1. Load file

* Load DICOM file

```

dicom_image, flipflag, Seriesdesc, thickness, spacing = load_dcm(dicom_path, information_flag = True)

dicom_image, flipflag = load_dcm(dicom_path, information_flag = False)

flip_flag는 dicom header의 orientation을 확인하여 나중에 nifti 파일로 저장할때 flip을 해주기 위한 flag이다.


```

* Load Nifti file

```
nii, affine, header = load_nii(nifti_path)
```



## 2. Convert format function

* Convert DICOM to Nifti

```
dcm2nii(ref_dicom_dir, save_nii_dir, file_name, volume, flip_flag)
* ref_dicom_dir : dicom file directory
* save_nii_dir  : nifti file save directory
* file_name     : nifti file name
* volume        : CT volume array
* flip_flag     : load_dcm에서 받은 flip_flag

```


* Convert Nifti to DICOM

```
nii2dcm(ref_dicom_dir, target_nii_file, volume)
* ref_dicom_dir : original dicom dir
* target_nii_file : nifti file path
* volume : CT volume array
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
