import time
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import numpy as np
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
import glob

import os
os.chdir('/opt/project')

flags.DEFINE_string('classes', './data/voc2012.names', 'path to classes file')
flags.DEFINE_string('weights', './checkpoints/yolov3_train_47.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('imagesPath', './data/voc2012_raw/VOCdevkit/VOC2012/ForMAP/Images/', 'path ')
flags.DEFINE_string('detectionResultPath', './data/voc2012_raw/VOCdevkit/VOC2012/ForMAP/DetectionResults', 'path')
flags.DEFINE_string('tfrecord', None, 'tfrecord instead of image')
flags.DEFINE_string('output', './output.jpg', 'path to output image')
flags.DEFINE_integer('num_classes', 20, 'number of classes in the model')


def main(_argv):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    for physical_device in physical_devices:
        tf.config.experimental.set_memory_growth(physical_device, True)

    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights).expect_partial()
    logging.info('weights loaded')

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    logging.info('classes loaded')

    image_list = glob.glob(FLAGS.imagesPath + '/*.jpg')
    for image in image_list:
        img_raw = tf.image.decode_image(open(image, 'rb').read(), channels=3)
        wh = np.flip(img_raw.shape[0:2])
        img = tf.expand_dims(img_raw, 0)
        img = transform_images(img, FLAGS.size)

        boxes, scores, classes, nums = yolo(img)

        file = open(FLAGS.detectionResultPath +'/' +image.split("/")[-1].replace(".jpg",".txt"), 'w')
        boxes, objectness, classes, nums = boxes[0], scores[0], classes[0], nums[0]

        for i in range(nums):
            x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
            x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
            file.write("{} {:.6f} {} {} {} {} \n".format(class_names[int(classes[i])], objectness[i],x1y1[0],x1y1[1],x2y2[0],x2y2[1]))
        file.close()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
