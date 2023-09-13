import glob
import nibabel as nib
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
import pdb

parser = argparse.ArgumentParser(description='Process args')
parser.add_argument('--path', type=str, help='entry path')
parser.add_argument('--datafolder', type=str, help='input data path')
parser.add_argument('--gtfolder', type=str, help='gt path')
parser.add_argument('--mergefolder', type=str, help='merge with gt path')
parser.add_argument('--outfolder', type=str, help='outfolder path')
args = parser.parse_args()

datafolder = args.datafolder
outfolder = args.outfolder
gtfolder = args.gtfolder
path = f'{args.path}{datafolder}/'

nii_files = glob.glob(os.path.join(path, '*.nii'))
os.makedirs(outfolder.join(path.rsplit(datafolder, 1)), exist_ok=True)

for nii_file in nii_files:
	nii_input = nib.load(nii_file)
	header = nii_input.header
	# voxel_sizes = header.get_zooms()
	id_ = os.path.basename(nii_file)[:-4]
	raw_files = []
	raw_files = glob.glob(gtfolder.join(path.rsplit(datafolder, 1)) + id_ + '_gt*.raw') # multiple class gt per id
	# raw_files = glob.glob(path.replace(datafolder, gtfolder) + id_ + "_gt[13].raw") # define which class
	if len(raw_files) == 0:
		print('No GT found!')
		pdb.set_trace()
	raw_files.sort()
	mask_out = np.zeros((nii_input.shape[2], nii_input.shape[1], nii_input.shape[0]))
	
	for i, raw_file in enumerate(raw_files, 1):
		cls = int(raw_file[raw_file.rfind('_gt')+3:raw_file.rfind('.')])
		# cls = i
		mask = np.fromfile(raw_file, dtype='uint8', sep="")
		mask = mask.reshape(mask_out.shape)
		mask_out = np.where(mask, cls, mask_out)

		if args.mergefolder:
			merge = np.fromfile(raw_file.replace(gtfolder, args.mergefolder, 1), dtype='uint8', sep="")
			merge = merge.reshape(mask_out.shape)
			mask_out = np.where(merge, cls, mask_out)
		print(raw_file, cls)
	# mask_out = np.transpose(mask_out, axes=[2, 0, 1])
	nii = nib.Nifti1Image(np.transpose(mask_out.astype(np.int16), axes=[2, 1, 0]), affine=None, header=header)
	# idx = [0,1,3,2,4,5,6,7]
	# nii.header['pixdim'] = header['pixdim'][idx]
	# nib.save(nii, os.path.join(raw_file[:-8] + '.nii.gz'))
	nib.save(nii, os.path.join(outfolder.join(nii_file.rsplit(datafolder, 1)).replace('.nii', '.nii.gz')))
	# print(raw_file[:-8] + '.nii.gz', 'saved')
	print(nii_file[:-4] + '.nii.gz', 'saved')
