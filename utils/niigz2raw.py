import glob
import nibabel as nib
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
import pdb

parser = argparse.ArgumentParser(description='Process args')
parser.add_argument('--path', type=str, help='entry path')
parser.add_argument('--n_cls', type=int, help='number of class')
parser.add_argument('--target_cls', default=1, type=int, help='target class to convert')
args = parser.parse_args()

path = f'{args.path}/inference*/niigz/'
epochs = glob.glob(path)
for epoch in epochs:
	nii_files = glob.glob(os.path.join(epoch, '*.nii.gz'))
	os.makedirs(epoch.replace('niigz', 'raw'), exist_ok=True)

	for nii_file in nii_files:
		out_file = nii_file.replace('niigz', 'raw')
		nii_input = nib.load(nii_file)
		header = nii_input.header
		arr = np.transpose(np.array(nii_input.dataobj), axes=[2, 1, 0])
		# unique = np.unique(arr)
		# arr = arr[::-1, :, :] # reverse axis 0

		for i in range(args.target_cls, args.n_cls + 1):
			# if i == 0:
			# 	mask = np.where(arr == i, 0, 0)
			# else:
			mask = np.where(arr == i, 1, 0)
			#fileobj = open(f'{out_file[:-7]}_gt{i}.raw', mode='wb')
			fileobj = open(f'{out_file[:-7]}.raw', mode='wb')
			off = np.array(mask, dtype=np.uint8)
			off.tofile(fileobj)
			fileobj.close()

			#print(f'{out_file[:-7]}_gt{i}.raw', 'saved')
			print(f'{out_file[:-7]}.raw', 'saved')
