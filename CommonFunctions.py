
import os
import shutil
import cv2
import xml.etree.ElementTree

def MakeAndCleanDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        shutil.rmtree(dir)
        os.mkdir(dir)

def SaveImageWithBounidngBox(imageFileDir,saveDir):
    files = os.listdir(imageFileDir)
    imageFiles=[]
    for i in range(0,len(files)):
        if ".bmp" in files[i]:
            imageFiles.append(files[i])
    i=0

    for j in range(0,len(imageFiles)):
        xml_name = imageFiles[j].replace('bmp', 'xml')
        meta = xml.etree.ElementTree.parse(imageFileDir + "/" + xml_name).getroot()
        true_bndbox = {}
        true_bndbox['xmin'] = 0
        true_bndbox['xmax'] = 0
        true_bndbox['ymin'] = 0
        true_bndbox['ymax'] = 0
        if meta is not None:
            obj = meta.find('object')
            if obj is not None:
                box = obj.find('bndbox')
                if box is not None:
                    true_bndbox['xmin'] = int(box.find('xmin').text)
                    true_bndbox['xmax'] = int(box.find('xmax').text)
                    true_bndbox['ymin'] = int(box.find('ymin').text)
                    true_bndbox['ymax'] = int(box.find('ymax').text)

        img = cv2.imread(os.path.join(imageFileDir,imageFiles[j]))
        cv2.rectangle(img, (int(true_bndbox['xmin']), int(true_bndbox['ymin'])), (int(true_bndbox['xmax']), int(true_bndbox['ymax'])),(255, 255, 0), 2)
        cv2.imwrite(saveDir+"/"+imageFiles[j], img)