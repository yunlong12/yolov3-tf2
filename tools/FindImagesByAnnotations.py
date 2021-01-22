
import glob
import shutil
import os
os.chdir('/opt/project')

annotationPath = './data/VOCTest/VOC2012/Annotations'
imagesPath = './data/VOCTest/VOC2012/JPEGImages'
annotationList = glob.glob(annotationPath+ '/*.xml')

for oneAnnotation in annotationList:
    imageName = oneAnnotation.split('/')[-1].replace(".xml",".jpg")
    fullImagePath = os.path.join(imagesPath,imageName)
    targeImagePath = fullImagePath.replace("JPEGImages","JPEGImagesForTest")
    shutil.copyfile(fullImagePath,targeImagePath)
