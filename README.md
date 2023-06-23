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

---

## 3. CT array plot function


* 3D plot

```
plot_3d(array, axis,title = '',  projection_flag = False,sub1_title = '', sub2_title = '', sub3_title = '')
 
* array : CT volume array
* axis : plot axis
* title : plot title
* projection_flag : projection plot flag
* sub1_title : subplot 1 title
* sub2_title : subplot 2 title
* sub3_title : subplot 3 title
```
if projection_flag is False, plot 3D plot
![image](https://github.com/HongYongGi/DICOM_file_function/assets/39263586/676fcd38-cb54-4eb7-9df3-2efe2b3771d7)

if projection_flag is True, plot 3D projection plot
![image](https://github.com/HongYongGi/DICOM_file_function/assets/39263586/df2fb496-54a1-4a0f-8f0c-39e41b7c84f4)



* 3D animate volume plot


```
animate_3d(image, threshold=-300)
* image : CT volume array
* threshold : threshold value
```
![image](https://github.com/HongYongGi/DICOM_file_function/assets/39263586/c3518615-5b0b-486f-bb2a-d06f1f841100)