import nibabel as nib
import matplotlib.pylab as plt
import numpy as np

WM_THRESHHOLD = 400

flair = "SET FLAIR DATA PATH HERE"
mri = nib.load(flair).get_fdata()
img_count = mri.shape[2]
print(img_count)


bw_MRI = []
for i in range(img_count):
    bw_img = []
    for r in mri[:,:,i]:
        bw_row = []
        for ci in r:
            if ci > WM_THRESHHOLD:
                ci = 1
            else:
                ci = 0
            bw_row.append(ci)
        bw_img.append(bw_row)
    bw_MRI.append(bw_img)

np_bw_MRI = np.asarray(bw_MRI)

f, a = plt.subplots(8, 8, figsize=(20,20))
for i, a in enumerate(a.reshape(-1)):
    a.imshow(np_bw_MRI[i + 20,:,:])

plt.show()

f, a = plt.subplots(8, 8, figsize=(20,20))
for i, a in enumerate(a.reshape(-1)):
    a.imshow(mri[:,:,i + 5])

plt.show()


# f, a = plt.subplots(12, 12, figsize=(20,20))
# for i, a in enumerate(a.reshape(-1)):
#     a.imshow(mri[:,:,i])

# plt.show()