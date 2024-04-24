import keras_model as km
import keras
from pyspark import SparkConf, SparkContext
import horovod.keras as hvd
import tensorflow as tf
from keras.callbacks import CSVLogger

print("> Initializing pyspark")
conf = SparkConf().setAppName("CONFIGURE APP NAME HERE")
conf.setMaster("CONFIGURE SPARK MASTER NODE HERE")
spark = SparkContext.getOrCreate(conf)

print("> Intitializing horovod")
hvd.init()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = str(hvd.local_rank())
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

print("> Setting optimizer")
opt = keras.optimizers.Adadelta(1.0 * hvd.size())
opt = hvd.DistributedOptimizer(opt)

print("> Building model")
model = km.custom_model()

print("> Setting callbacks")
callbacks = [hvd.callbacks.BroadcastGlobalVariablesCallback(0),]
if hvd.rank() == 0:
    callbacks.append(keras.callbacks.ModelCheckpoint('./out/checkpoint_{epoch}.h5'))
logger = CSVLogger('CONFIGURE OUTPUT PATH HERE', append=True, separator=',')
callbacks.append(logger)

print("> Training...")
km.train(model, "CONFIGURE DATA PATH HERE", "CONFIGURE SEG PATH HERE", "CONFIGURE SAVE PATH HERE", callbacks=callbacks)

km.use(model, "CONFIGURE DATA PATH HERE", "CONFIGURE SAVE PATH HERE", "SET OUTPUT NAME HERE")