import os

import numpy as np
import matplotlib as plt
from PIL import Image
import image_processing as imp

import keras
import cv2
import keras_segmentation.predict as ksp
from keras_segmentation.models.model_utils import get_segmentation_model
import keras_segmentation.models.all_models as models


# Builds and returns custom Keras model for training
def custom_model():
    img_in = keras.Input(shape=(240,240,1))
    c1 = keras.layers.Conv2D(24, (3,3), activation='relu', padding='same')(img_in)
    c1 = keras.layers.Dropout(0.2)(c1)
    c1 = keras.layers.Conv2D(24, (3,3), activation='relu', padding='same')(c1)
    p1 = keras.layers.MaxPooling2D((2,2))(c1)

    c2 = keras.layers.Conv2D(48, (3,3), activation='relu', padding='same')(p1)
    c2 = keras.layers.Dropout(0.2)(c2)
    c2 = keras.layers.Conv2D(48, (3,3), activation='relu', padding='same')(c2)
    p2 = keras.layers.MaxPooling2D((2,2))(c2)

    c3 = keras.layers.Conv2D(96, (3,3), activation='relu', padding='same')(p2)
    c3 = keras.layers.Dropout(0.2)(c3)
    c3 = keras.layers.Conv2D(96, (3,3), activation='relu', padding='same')(c3)

    u1 = keras.layers.concatenate([keras.layers.UpSampling2D((2,2))(c3), c2], axis=-1)
    c4 = keras.layers.Conv2D(48, (3,3), activation='relu', padding='same')(u1)
    c4 = keras.layers.Dropout(0.2)(c4)
    c4 = keras.layers.Conv2D(48, (3,3), activation='relu', padding='same')(c4)

    u2 = keras.layers.concatenate([keras.layers.UpSampling2D((2,2))(c4), c1], axis=-1)
    c5 = keras.layers.Conv2D(24, (3,3), activation='relu', padding='same')(u2)
    c5 = keras.layers.Dropout(0.2)(c5)
    c5 = keras.layers.Conv2D(24, (3,3), activation='relu', padding='same')(c5)

    out = keras.layers.Conv2D( 4, (1,1), padding='same')(c5)

    return get_segmentation_model(img_in, out)

# Builds and returns a pretrained model
def prebuilt_model(sel, w=480, h=480):
    if sel == "resnet":
        return models.segnet.resnet50_segnet(4, w, h, channels=1)
    elif sel == "vgg":
        return models.unet.vgg_unet(4, w, h, channels=1)
    elif sel == "mnet":
        return models.segnet.mobilenet_segnet(4, w, h, channels=1)
    else:
        print("Model selection not valid defaulting to custom model")
        return custom_model()
    
def load_model(checkpoint_path, m_name="", weight_file=None):
    return ksp.model_from_checkpoint_path(checkpoint_path, weight_file), m_name

def train(model, data_path, ann_path, checkpoint_path=None, epochs=5, steps=50, callbacks=None, verify=False):
    model.train(
        train_images = data_path,
        train_annotations = ann_path,
        checkpoints_path = checkpoint_path,
        verify_dataset = verify,
        callbacks=callbacks,
        epochs = epochs,
        steps_per_epoch = steps,
        read_image_type=0 #Greyscale image
    )

def evaluate(model, data_path, ann_path):
    in_imgs = _get_image_paths(data_path)
    seg_imgs = _get_image_paths(ann_path)

    all_pres = []
    all_recall = []
    all_acc = []

    for i in range(len(in_imgs)):
        img_in = imp.open_img(in_imgs[i])
        out = imp.convert_output(_make_prediction(model, np.asarray(img_in).reshape(240,240,1)))
        seg_img = imp.open_img(seg_imgs[i])

        tp = 0 # True positives
        fp = 0 # False positives
        fn = 0 # False negative
        err = 0

        empty_img = True
        n_none_empty = 0
        for row_index in range(len(out)):
            for pixel_index in range(len(out[row_index])):
                out_pix = out[row_index][pixel_index]
                true_pix = seg_img[row_index][pixel_index]


                if true_pix > 0:
                    empty_img = False
                    n_none_empty += 1

                if out_pix == true_pix and true_pix != 0:
                    tp += 1
                elif out_pix > 0 and true_pix == 0:
                    fp += 1
                elif out_pix == 0 and true_pix > 0:
                    fn += 1  

                if out_pix != true_pix:
                    err += 1

        if not empty_img:
            if (tp + fp) == 0:
                precision = 'NA'
            else:
                precision = float(tp) / float(tp + fp)
                all_pres.append(precision)
            if (tp + fn) == 0:
                recall = 'NA'
            else:
                recall = float(tp) / float(tp + fn)
                all_recall.append(recall)
            accuracy = float(tp) / n_none_empty
            all_acc.append(accuracy)

            print(f'Precision: {precision}, Recall: {recall}, Accuracy: {accuracy}')

    mean_p = calc_mean(all_pres)
    mean_r = calc_mean(all_recall)
    mean_a = calc_mean(all_acc)

    return f'MEANS: Precision: {mean_p}, Recall: {mean_r}, Accuracy: {mean_a}'


def calc_mean(numeric_list):
    total = 0.0
    for val in numeric_list:
        total += val
    return total / len(numeric_list)

def use(model, scan_in, save_path, f_name):
    if scan_in[-4:] == '.png':
        print("Found single image")
    else:
        print("Assuming directory input")
        scan_in = _get_image_paths(scan_in)

    if isinstance(scan_in, list):
        for i in range(len(scan_in)):
            if i % 100 == 0:
                print("Saving image #" + str(i))
            img = _read_img(scan_in[i])
            out = _make_prediction(model, img)
            out_img = _build_new_image(out)
            _save_img(out_img, save_path, f_name + str(i))
    else:
        print("Saving image")
        img = _read_img(scan_in)
        out = _make_prediction(model, img)
        out_img = _build_new_image(out)
        _save_img(out_img, save_path, f_name)

def _get_image_paths(data_path):
    file_paths = []
    for entry in os.listdir(data_path):
        if entry[-4:] == '.png':
            path = os.path.join(data_path, entry)
            file_paths.append(path)
    return(file_paths)
            
def _read_img(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = img.reshape(240, 240, 1)
    return img

def _make_prediction(model, img):
    return ksp.predict(
        model=model,
        inp=img,
        read_image_type=0
    )

def _build_new_image(img_data):
    new_image = []
    for r in img_data:
        new_row = []
        for p in r:
            if p == 3:
                new_row.append(255)
            elif p == 2:
                new_row.append(127)
            elif p == 1:
                new_row.append(63)
            else:
                new_row.append(0)
        new_image.append(new_row)
    return new_image

def _save_img(img_data, save_path, f_name):
    img = np.array(img_data)
    print(img.shape)
    img = Image.fromarray(img)
    img = img.convert('L')
    img.save(save_path + '/' + f_name + '.png')