import sys
from PIL import Image
import os
from threading import *
from datetime import datetime
import optparse

# Keeping the output cleaned 
screenLock = Semaphore(value=1)

# save images into this directory
directory = "converted"

# output messages
def message(file, bool, targetExt, fileName):
    screenLock.acquire()
    # if converted
    if bool:
        print(datetime.now().time().strftime('%H:%M:%S') + " Converted: " + fileName + targetExt)
    else:
        print(datetime.now().time().strftime('%H:%M:%S') + " Converting:  " + file + " \t-> " + fileName + targetExt)
    screenLock.release()

# create directory
if not os.path.exists(directory):
    os.makedirs(directory)

# convert raw images function
def convert(file, fileName, fileExt, rawDir, targetDir, rawExt="all", targetExt=".jpg"):
    # only convert selected extension files
    if (rawExt == 'all'):
        try:
            message(file, False, targetExt, fileName)
            path = os.path.join(rawDir, file)
            im = Image.open(path)
            im.save(os.path.join(directory, fileName + targetExt))
            message(file, True, targetExt, fileName)
        except:
            pass
    else: 
        if (fileExt == rawExt):
            try:
                message(file, False, targetExt, fileName)
                path = os.path.join(rawDir, file)
                im = Image.open(path)
                im.save(os.path.join(directory, fileName + targetExt))
                message(file, True, targetExt, fileName)
            except:
                pass

# checks for images to be converted
def not_exists(fileName, ext):
    #print(fileName)
    if os.path.isfile(os.path.join(directory, fileName + ext)):
        screenLock.acquire()
        print("File " + fileName + ext + " is already converted!")
        screenLock.release()
        return False
    else:
        return True

# MAIN
def main():
    parser = optparse.OptionParser("Use: python " + sys.argv[0] + " --d <raw directory> --rext <rawExtension(default='all')> --text <targetExtension(default='.jpg')>")

    parser.add_option('--d', dest='nname', type='string')
    parser.add_option('--rext', dest='rawextension', type='choice', default="all", choices = ['all', '.tif', '.tiff', '.bmp', '.jpg', '.png', '.jpeg'])
    parser.add_option('--text', dest='targetextension', type='choice', default=".jpg", choices = ['.tif', '.tiff', '.bmp', '.jpg', '.png', '.jpeg'])

    (options, args) = parser.parse_args()
    if (options.nname == None):
        print(parser.usage)
        exit(0)
    else:
        rawDir = os.path.abspath(options.nname)

    print("Started conversion at : " + datetime.now().time().strftime('%H:%M:%S') + '\n')
    print("Converting " + options.rawextension + " files to " + options.targetextension + " in the directory: \n -> " + rawDir + "\n")
    print(" \n Converted " + options.targetextension + " images are stored at:\n -> " + os.path.abspath(directory) + "\n")

    # find files to convert
    try:
        for file in os.listdir(rawDir):
            fileArr = file.split('.')
            x = len(fileArr)
            fileName = file.split('.' + fileArr[x-1])
            fileExt = '.' + fileArr[x-1]
            fileName = fileName[0]
            # checks images in converted directory
            if not_exists(fileName, options.targetextension):
                # multithread processing
                t = Thread(target=convert, args=(file, fileName, fileExt, rawDir, directory, options.rawextension, options.targetextension))
                t.start()  
    except:
        print(
            "\n The directory at: \n " + rawDir + "  \n does not exists")

if __name__ == '__main__':
    main()