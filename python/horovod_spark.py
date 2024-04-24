import horovod.keras as hvd
import keras
import keras_model as km
from keras import backend as k
from keras.callbacks import CSVLogger
import tensorflow as tf
from pyspark import SparkConf, SparkContext

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

print("> Setting optimizer")
opt = keras.optimizers.Adadelta(1.0 * hvd.size())
opt = hvd.DistributedOptimizer(opt)

print("> Building models")
# model_flair_custom = km.custom_model()
# model_flair_resnet = km.prebuilt_model("resnet")
model_flair_vgg = km.prebuilt_model("vgg")
# model_flair_mnet = km.prebuilt_model("mnet")

# model_t1_custom = km.custom_model()
# model_t1_resnet = km.prebuilt_model("resnet")
model_t1_vgg = km.prebuilt_model("vgg")
# model_t1_mnet = km.prebuilt_model("mnet")

all_models = [model_t1_vgg]#, model_t1_vgg]#, model_flair_resnet, model_flair_vgg, model_flair_mnet, model_t1_custom, model_t1_resnet, model_t1_vgg, model_t1_mnet]
out_names = ["250_vgg_t1"]#, "250_vgg_t1"]#, "model_flair_resnet", "model_flair_vgg", "model_flair_mnet", "model_t1_custom", "model_t1_resnet", "model_t1_vgg", "model_t1_mnet"]

for i in range(len(all_models)):
    print("> Setting callbacks: " + out_names[i])
    callbacks = [hvd.callbacks.BroadcastGlobalVariablesCallback(0),]
    if hvd.rank() == 0:
        callbacks.append(keras.callbacks.ModelCheckpoint('./out/' + out_names[i] + '/' + out_names[i] + '_{epoch}.h5'))
    logger = CSVLogger('./out/' + out_names[i] + '/training_log.csv', append=True, separator=',')
    callbacks.append(logger)

    print("> Training: " + out_names[i])
    if i > 1:
        km.train(all_models[i], './data_sets/flair_data/train_in', './data_sets/flair_data/train_out', './out/' + out_names[i] + '/', epochs=5, steps=10, callbacks=callbacks)
    else:
        km.train(all_models[i], './data_sets/t1ce_data/train_in', './data_sets/t1ce_data/train_out', './out/' + out_names[i] + '/', epochs=5, steps=10, callbacks=callbacks)
