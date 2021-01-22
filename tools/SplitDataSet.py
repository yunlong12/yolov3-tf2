
import os
import glob
import random
import shutil
import time
import os
import hashlib
from absl import app, flags, logging
from absl.flags import FLAGS
import tensorflow as tf
import lxml.etree
import tqdm
from CommonFunctions import MakeAndCleanDir

os.chdir('/opt/project')

flags.DEFINE_string('data_dir', "data/voc2012_raw/VOCdevkit/VOC2012/JPEGImages",
                    'path to Polyps data set for training, validation and test')
flags.DEFINE_string('fraction', '80:20:0', 'fraction as train:valid:test')


def split_data_set(data_dir, fraction): # fraction as train:valid:test
    import json, random, glob
    data_list = glob.glob(os.path.join(data_dir, "*.jpg"))
    data_list = [[img_path, img_path.replace("jpg","xml").replace("JPEGImages","Annotations")] for img_path in data_list]
    whole_frac, data_list_len = 0, len(data_list)
    for frac in fraction: whole_frac += frac
    num_list = [int(data_list_len*frac/whole_frac) for frac in fraction]
    random.shuffle(data_list)
    data_set_list = {}
    data_set_list["train"] = data_list[:num_list[0]] # train set
    data_set_list["valid"] = data_list[num_list[0]:num_list[0] + num_list[1]]  # valid set

    file = open('data/voc2012_raw/VOCdevkit/VOC2012/ImageSets/Main/trainMy.txt', 'w')
    for i in data_set_list["train"]:
        str=i[0].split("/")[-1].replace(".jpg","")+"\n"
        file.write(str)
    file.close()

    file = open('data/voc2012_raw/VOCdevkit/VOC2012/ImageSets/Main/validMy.txt', 'w')
    for i in data_set_list["valid"]:
        str=i[0].split("/")[-1].replace(".jpg","")+"\n"
        file.write(str)
    file.close()

    data_set_list["test"] = data_list[num_list[0]+num_list[1]:] # test set
    logging.info(
        "\n# of train data: {}\n # of valid data: {}\n # of test data: {}\n".format(
            len(data_set_list["train"]),len(data_set_list["valid"]),len(data_set_list["test"])
        )
    )
    #with open('./data/data_set_list.json', 'w') as fp:
        #json.dump(data_set_list, fp, indent=4)
    return data_set_list

def CopyFilesIntoSubDatset(subDatasetName,data_set_list):
    fileDir=FLAGS.data_dir+"_"+subDatasetName
    MakeAndCleanDir(fileDir)

    for file in data_set_list[subDatasetName]:
        shutil.copy(file[0], fileDir)
        shutil.copy(file[1], fileDir)

def main(_argv):
    fraction = FLAGS.fraction.split(":")
    fraction = [float(frac) for frac in fraction]
    data_set_list = split_data_set(FLAGS.data_dir, fraction)

    #CopyFilesIntoSubDatset(subDatasetName="train",data_set_list=data_set_list)
    #CopyFilesIntoSubDatset(subDatasetName="valid", data_set_list=data_set_list)
    #CopyFilesIntoSubDatset(subDatasetName="test", data_set_list=data_set_list)

if __name__ == '__main__':
    app.run(main)