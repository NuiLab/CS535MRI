import nibabel as nib
import matplotlib.pylab as plt
import numpy as np
import gzip
from PIL import Image
import os
import shutil
import random
import imageio.v3 as imio

def get_MRI_rec(path='.', file_paths=[]):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            get_MRI_rec(full_path, file_paths)
        else:
            file_paths.append(full_path)
    return file_paths

def extract_mri_niis(save_path='.', file_paths=[str]):
    for p in file_paths:
        with gzip.open(p, 'rb') as gzf:
            f_name = str.split(p, '\\')
            d_set, p_id, mri_type = str.split(f_name[-1], '_')
            mri_type = str.split(mri_type, '.')[0]
            file_save_path = "{}/{}_{}.nii".format(save_path, p_id, mri_type)
            with open(file_save_path, 'wb') as save:
                while True:
                    block = gzf.read()
                    if not block:
                        break
                    else:
                        save.write(block)
                        
def get_nii_max(nii_memmap):
    max = 0.0
    for i in range(nii_memmap.shape[2]):
        scan_data = nii_memmap[:,:,i]
        scan_max = np.max(scan_data)
        if scan_max > max:
            max = scan_max
    return max

def img_normalize(img_data, nii_max):
    norm_img_data = 255 * (img_data/nii_max)
    return norm_img_data

def save_nii_imgs(save_path='.', file_paths=[str], gt_threshold=None, gt_max=None):
    im_count = 0
    for nii_path in file_paths:

        if im_count % 5 == 0:
            print("Saving image number: " + str(im_count))
        im_count += 1

        nii = nib.load(nii_path).get_fdata()
        nii_max = get_nii_max(nii)

        f_name = str.split(nii_path, '\\')
        d_set, p_id, mri_type = str.split(f_name[-1], '_')
        mri_type = str.split(mri_type, '.')[0]

        for i in range(nii.shape[2]):
            img_data = nii[:,:,i]
            img_data_normalized = img_normalize(img_data, nii_max)

            if gt_threshold != None:
                gt_data = []
                for r in img_data_normalized:
                    gt_row = []
                    for c in r:
                        if (gt_max is not None) and (c > gt_max):
                            gt_row.append(0)
                        elif c > gt_threshold:
                            gt_row.append(255)
                        else:
                            gt_row.append(0)
                    gt_data.append(gt_row)
                img = Image.fromarray(np.asarray(gt_data))
                img = img.convert('L')
                img.save("{}/{}_{}_GT_slice-{}.png".format(save_path, p_id, mri_type, i))

            else:
                img = Image.fromarray(img_data_normalized)
                img = img.convert('L')
                img.save("{}/{}_{}_slice-{}.png".format(save_path, p_id, mri_type, i))

def img_details(img_path):
    img = imio.imread(img_path )
    print(img.shape)
    print(type(img))
    for r in img:
        print(r)

def split_data(data_path, ann_path, train_x, train_y, val_x, val_y, test_x, test_y):
    file_paths = []
    for entry in os.listdir(data_path):
        f_path = os.path.join(data_path, entry)
        file_paths.append(f_path)

    ann_file_paths = []
    for entry in os.listdir(ann_path):
        f_path = os.path.join(ann_path, entry)
        ann_file_paths.append(f_path)

    indicies = list(range(len(file_paths)))
    n_samples = int(len(file_paths) / 5)

    copycount = 0

    print("Copying validation set...")
    val_i = random.sample(indicies, n_samples)
    for i in val_i:
        indicies.remove(i)
        shutil.copy(file_paths[i], val_x)
        shutil.copy(ann_file_paths[i], val_y)
        if copycount % 100 == 0:
            print("> Copying file #" + str(copycount))
        copycount += 1

    print("Copying test set...")
    test_i = random.sample(indicies, n_samples)
    for i in test_i:
        indicies.remove(i)
        shutil.copy(file_paths[i], test_x)
        shutil.copy(ann_file_paths[i], test_y)
        if copycount % 100 == 0:
            print("> Copying file #" + str(copycount))
        copycount += 1

    print("Copying train set...")
    train_i = indicies
    for i in train_i:
        shutil.copy(file_paths[i], train_x)
        shutil.copy(ann_file_paths[i], train_y)
        if copycount % 100 == 0:
            print("> Copying file #" + str(copycount))
        copycount += 1