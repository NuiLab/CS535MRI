import os
import image_processing as imp
# from pyspark import SparkConf, SparkContext

# print("> Initializing PySpark")
# conf = SparkConf().setAppName("class_counter")
# conf.setMaster("spark://cheyenne.cs.colostate.edu:30176")
# spark = SparkContext.getOrCreate(conf)

def calc_mean(numeric_list):
    if(len(numeric_list)) != 0:
        total = 0.0
        for val in numeric_list:
            total += val
        return total / len(numeric_list)
    else:
        return None

img_path = 'D:/CS535/CS535-Term-Project/MRI Data/data_sets/flair_data/val_out'

class_0_freqs = []
class_1_freqs = []
class_2_freqs = []
class_3_freqs = []

weighted_class_1_freqs = []
weighted_class_2_freqs = []
weighted_class_3_freqs = []

print("Getting images from path")

imgs = []
for entry in os.listdir(img_path):
    if entry[-4:] == '.png':
        path = os.path.join(img_path, entry)
        imgs.append(path)

print("Processing images...")

for i in range(len(imgs)):
    print(f'Processing image {i}')
    img = imp.open_img(imgs[i])

    c0_count = 0
    c1_count = 0
    c2_count = 0
    c3_count = 0

    seg_count = 0

    is_empty = True
    for r in img:
        for p in r:
            if p > 0:
                seg_count += 1
                is_empty = False

            if p == 0:
                c0_count += 1
            elif p == 1:
                c1_count += 1
            elif p == 2:
                c2_count += 1
            elif p == 3:
                c3_count += 1
    
    if not is_empty:

        c0_f = float(c0_count) / float(240 * 240)
        c1_f = float(c1_count) / float(240 * 240)
        c2_f = float(c2_count) / float(240 * 240)
        c3_f = float(c3_count) / float(240 * 240)



        class_0_freqs.append(c0_f)
        class_1_freqs.append(c1_f)
        class_2_freqs.append(c2_f)
        class_3_freqs.append(c3_f)

        wc1_f = float(c1_count) / float(seg_count)
        wc2_f = float(c2_count) / float(seg_count)
        wc3_f = float(c3_count) / float(seg_count)

        weighted_class_1_freqs.append(wc1_f)
        weighted_class_2_freqs.append(wc2_f)
        weighted_class_3_freqs.append(wc3_f)

        print(f'> C0:{c0_f} C1:{c1_f} C2:{c2_f} C3:{c3_f} w_C1:{wc1_f} w_C2:{wc2_f} w_C3:{wc3_f}')

print('Calculating means...')
c0_mean = calc_mean(class_0_freqs)
c1_mean = calc_mean(class_1_freqs)
c2_mean = calc_mean(class_2_freqs)
c3_mean = calc_mean(class_3_freqs)

wc1_mean = calc_mean(weighted_class_1_freqs)
wc2_mean = calc_mean(weighted_class_2_freqs)
wc3_mean = calc_mean(weighted_class_3_freqs)


print(f'>MEANS C0:{c0_mean} C1:{c1_mean} C2:{c2_mean} C3:{c3_mean} w_C1:{wc1_mean} w_C2:{wc2_mean} w_C3:{wc3_mean}')