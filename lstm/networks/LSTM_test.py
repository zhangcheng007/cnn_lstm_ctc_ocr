import tensorflow as tf
from .network import Network
from lstm.utils.config import  cfg



class LSTM_test(Network):
    def __init__(self, trainable=True):
        self.inputs = []

        self.data = tf.placeholder(tf.float32, shape=[None, None, cfg.NUM_FEATURES], name='data')
        self.time_step_len = tf.placeholder(tf.int32,[None], name='time_step_len')

        self.keep_prob = tf.placeholder(tf.float32)
        self.layers = dict({'data': self.data, 'time_step_len':self.time_step_len})
        self.trainable = trainable
        self.setup()

    def setup(self):
        (self.feed('data')
         .conv_single(3, 3, 32 ,1, 1, name='conv1',c_i=cfg.NCHANNELS)
         .conv_single(3, 3, 32 ,1, 1, name='conv2')
         .max_pool(2, 2, 2, 2, padding='VALID', name='pool1')

         .conv_single(3, 3, 128 ,1, 1, name='conv3')
         .conv_single(3, 3, 256 ,1, 1, name='conv4')
         .max_pool(2, 2, 2, 2, padding='VALID', name='pool2')

         .conv_single(3, 3, 1 ,1, 1, name='conv5',relu=False))

        (self.feed('conv5','time_step_len')
         .lstm(cfg.TRAIN.NUM_HID,cfg.TRAIN.NUM_LAYERS,name='logits',img_shape=[-1,cfg.IMG_SHAPE[0]//cfg.POOL_SCALE,cfg.NUM_FEATURES//cfg.POOL_SCALE]))
