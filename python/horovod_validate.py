import keras_model as km
import numpy as np

from pyspark import SparkConf, SparkContext
import horovod.keras as hvd
import tensorflow as tf

def validate_models(models, model_names, data_path, ann_path, save_path):
    means = []
    for i in range(len(models)):
        mean, steps = km.evaluate(models[i], data_path, ann_path)
        means.append(mean)
        path = save_path + '/' + model_names[i] + '_step_acc.csv'
        np.savetxt(path, steps, delimiter=",")

    path = save_path + '/all_accs.csv'
    np.savetxt(path, means, delimiter=",")


########################################################################################################################

print("> Initializing PySpark")
conf = SparkConf().setAppName("CONFIGURE APP NAME HERE")
conf.setMaster("CONFIGURE SPARK MASTER NODE HERE")
spark = SparkContext.getOrCreate(conf)

print("> Initializing horovod")
hvd.init()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = str(hvd.local_rank())
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

flair_names = ["model_flair_custom","model_flair_mnet","model_flair_resnet","model_flair_vgg"]
t_names = ["model_t1_custom","model_t1_mnet","model_t1_resnet","model_t1_vgg"]

out_path = "CONFIGURE OUTPUT PATH HERE"

flair_models = []

c_flair_model = km.custom_model()
c_flair_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
flair_models.append(c_flair_model)

mnet_flair_model = km.prebuilt_model("mnet")
mnet_flair_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
flair_models.append(mnet_flair_model)

resnet_flair_model = km.prebuilt_model("resnet")
resnet_flair_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
flair_models.append(resnet_flair_model)

vgg_flair_model = km.prebuilt_model("vgg")
vgg_flair_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
flair_models.append(vgg_flair_model)

t1_models = []

c_t1_model = km.custom_model()
c_t1_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
t1_models.append(c_t1_model)

mnet_t1_model = km.prebuilt_model("mnet")
mnet_t1_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
t1_models.append(mnet_t1_model)

resnet_t1_model = km.prebuilt_model("resnet")
resnet_t1_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
t1_models.append(resnet_t1_model)

vgg_t1_model = km.prebuilt_model("vgg")
vgg_t1_model.load_weights("CONFIGURE WEIGHTS TO LOAD HERE")
t1_models.append(vgg_t1_model)

validate_models(flair_models, flair_names, "CONFIGURE DATA PATH HERE", 
                "CONFIGURE SEG PATH HERE", out_path + 'flair_eval')

validate_models(t1_models, t_names, "CONFIGURE DATA PATH HERE", 
                "CONFIGURE SEG PATH HERE", out_path + "t1_eval")