import keras_model as km
import image_processing as imp
import os



## Check different models
# custom_flair = km.custom_model()
# custom_flair.load_weights("D:CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_flair_custom_5.h5")
# custom_t1 = km.custom_model()
# custom_t1.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_t1_custom_5.h5")

# resnet_flair = km.prebuilt_model('resnet')
# resnet_flair.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_flair_resnet_5.h5")
# resnet_t1 = km.prebuilt_model('resnet')
# resnet_t1.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_t1_resnet_5.h5")

# mnet_flair = km.prebuilt_model('mnet')
# mnet_flair.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_flair_mnet_5.h5")
# mnet_t1 = km.prebuilt_model('mnet')
# mnet_t1.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_t1_mnet_5.h5")

# vgg_flair = km.prebuilt_model('vgg')
# vgg_flair.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_flair_vgg_5.h5")
# vgg_t1 = km.prebuilt_model('vgg')
# vgg_t1.load_weights("D:/CS535/CS535-Term-Project/results/training_output/_model_compare_weights/model_t1_vgg_5.h5")

# model_tags = ['custom', 'resnet', 'mnet', 'vgg']

# flair_models = []
# flair_models.append(custom_flair)
# flair_models.append(resnet_flair)
# flair_models.append(mnet_flair)
# flair_models.append(vgg_flair)

# t1_models = []
# t1_models.append(custom_t1)
# t1_models.append(resnet_t1)
# t1_models.append(mnet_t1)
# t1_models.append(vgg_t1)


# km.use(flair_models[1], flair_test_img, save_path, 'initial_training_compare_flair_{}'.format(model_tags[1]))

# for i in range(len(model_tags)):
#     km.use(flair_models[i], flair_test_img, save_path, 'initial_training_compare_flair_{}'.format(model_tags[i]))
#     km.use(t1_models[i], t1_test_img, save_path, 'initial_training_compare_t1_{}'.format(model_tags[i]))

## Check different vgg weights

# vgg_flair_weight_path = "D:/CS535/CS535-Term-Project/results/training_output/_vgg_compare_weights/final_vgg_flair"

# vgg_t1_weight_path = "D:/CS535/CS535-Term-Project/results/training_output/_vgg_compare_weights/final_vgg_t1"

# vgg_250_flair_weight_path = "D:/CS535/CS535-Term-Project/results/training_output/_vgg_compare_weights/250_vgg_flair"

# vgg_flair = km.prebuilt_model('vgg')
# vgg_t1 = km.prebuilt_model('vgg')

# flair_weight_files = os.listdir(vgg_flair_weight_path)
# t1_weight_files = os.listdir(vgg_t1_weight_path)
# flair_250_files = os.listdir(vgg_250_flair_weight_path)

# for i in range(len(flair_250_files)):
#     print(flair_250_files[i])
#     vgg_flair.load_weights('{}/{}'.format(vgg_250_flair_weight_path, flair_250_files[i]))
#     km.use(vgg_flair, flair_test_img, save_path, '250_compare_{}'.format(flair_250_files[i][:-3]))

# for i in range(len(t1_weight_files)):
#     vgg_t1.load_weights('{}/{}'.format(vgg_t1_weight_path, t1_weight_files[i]))
#     km.use(vgg_t1, t1_test_img, save_path, 'compare_{}'.format(t1_weight_files[i][:-3]))

## Spit out 5 image sets

# flair_test_img = "D:/CS535/CS535-Term-Project/results/gen_in_imgs/00002_slice-78.png"
# t1_test_img = "D:/CS535/CS535-Term-Project/MRI Data/t1ce_images/00002_slice-78.png"
# save_path = "D:/CS535/CS535-Term-Project/results/processed_images"

# final_weights = "D:/CS535/CS535-Term-Project/results/refined_models/final_vgg_flair/final_vgg_flair_30.h5"
# img_path = "D:/CS535/CS535-Term-Project/results/gen_in_imgs"
# img_files = os.listdir(img_path)

# model = km.prebuilt_model('vgg')
# model.load_weights(final_weights)

# for i in img_files:
#     km.use(model, f'{img_path}/{i}', save_path, f'out_{i[:-4]}')