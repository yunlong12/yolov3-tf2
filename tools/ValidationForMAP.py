
import os
import shutil

validationFilePath = 'data/voc2012_raw/VOCdevkit/VOC2012/ImageSets/Main/validMy.txt'
annotationFolder = 'data/voc2012_raw/VOCdevkit/VOC2012/Annotations'
imagesFolder = 'data/voc2012_raw/VOCdevkit/VOC2012/JPEGImages'

mAPBasicPath = 'data/voc2012_raw/VOCdevkit/VOC2012/ForMAP'
mAPGT = os.path.join(mAPBasicPath,'GroundTruth')
mAPDR = os.path.join(mAPBasicPath,'DetectionResults')
mAPImages = os.path.join(mAPBasicPath,'Images')

os.chdir('/opt/project')

"""
 Convert the lines of a file to a list
"""
def file_lines_to_list(path):
    # open txt file lines to a list
    with open(path) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

fileList = file_lines_to_list(validationFilePath)
for file in fileList:
    shutil.copy(os.path.join(annotationFolder,file+".xml"),os.path.join(mAPGT,file+".xml"))
    shutil.copy(os.path.join(imagesFolder,file+".jpg"),os.path.join(mAPImages,file+".jpg"))
