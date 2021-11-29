import sys
import PIL
from PIL import Image
import os
from threading import *
from datetime import datetime
import optparse

# Keeping the output cleaned 
screenLock = Semaphore(value=1)

# save images into this directory
directory = "transformed"
if not os.path.exists(directory):
    os.makedirs(directory)

# MAIN
def main():

    # option/argument handling
    parser = optparse.OptionParser("Use: python " + sys.argv[0] + " -d/--dir <raw directory> -r/--rright <rotate right (float) default=0> -l/--rleft <rotate left (float) default=0> -e/--expand (expands the output image to make it large enough to hold the entire rotated image (bool)) -v/--fvert (flip vertical (bool)) -f/--fhor (flip horizontal (bool)) -W/--width <new width (int)> -H/--height <new height (int)> -a/--aratio (keep aspect ratio (bool)) -o/--order <change the order of transformation tasks (s=size, f=flip, r=rotate) default='sfr'")
    
    parser.add_option('-d', '--dir', dest='nname', type='string')
    parser.add_option('-r', '--rright', dest='rotateright', type='float', default=0)
    parser.add_option('-l', '--rleft', dest='rotateleft', type='float', default=0)
    parser.add_option('-e', '--expand', action="store_true", dest='expand', default=False)
    parser.add_option('-v', '--fvert', action="store_true", dest='flipvert', default=False)
    parser.add_option('-f', '--fhor', action="store_true", dest='fliphor', default=False)
    parser.add_option('-W', '--width', dest='width', type='int', default=0)
    parser.add_option('-H', '--height', dest='height', type='int', default=0)
    parser.add_option('-a', '--aratio', action="store_true", dest='aspectratio', default=False)
    parser.add_option('-o', '--order', dest='order', type='string', default='sfr')

    (options, args) = parser.parse_args()
    if (options.nname == None):
        print(parser.usage)
        exit(0)
    else:
        rawDir = os.path.abspath(options.nname)
    flip = [options.flipvert, options.fliphor]
    angle = options.rotateleft - options.rotateright
    newWidth = options.width
    newHeight = options.height
    print("Started transformation at : " + datetime.now().time().strftime('%H:%M:%S') + '\n')

    # generating file name suffix
    transformstr = ""

    if (options.flipvert == 1):
        transformstr += "_vertical"
        print("Flipping files vertically\n")
    if (options.fliphor == 1):
        transformstr += "_horizontal"
        print("Flipping files horizontally\n")

    if (angle > 0):
        print("Rotating files to the left by " + str(angle%360) + " degrees.\n")
        transformstr += "_left_"+str(angle%360)
    if(angle < 0):
        print("Rotating files to the right by " + str(-angle%360) + " degrees.\n")
        transformstr += "_right_"+str(-angle%360)
    if(options.expand == True):
        print("Expanding image after rotation\n")
        transformstr += "_ex"

    if((newHeight == 0 or newWidth == 0) and not(newHeight == 0 and newWidth == 0)):
        if(newWidth == 0):
            print("Resizing images to (Width x Height) default x " + str(newHeight) + "\n")
            transformstr += "_x" + str(newHeight)
        if(newHeight == 0):
            print("Resizing images to (Width x Height) " + str(newWidth) + " x default\n")
            transformstr += "_" + str(newWidth) + "x"
    if(newHeight != 0 and newWidth != 0):
        if(options.aspectratio == False):
            print("Resizing images to (Width x Height) " + str(newWidth) + " x " + str(newHeight) +"\n")
            transformstr += "_" + str(newWidth) + "x" + str(newHeight)
        else:
            print("Resizing images to (Width x Height) " + str(newWidth) + " x\n")
            transformstr += "_" + str(newWidth) + "x"
    if(options.aspectratio == True):
        print("Keeping aspect ratio\n")
        transformstr += "_ar"

    transformstr += "_" + options.order
    print("Saved files in directory: '" + directory + "' as FILENAME_" + transformstr + ".EXTENSION")

    # find files to transform
    try:
        for file in os.listdir(rawDir):
            fileArr = file.split('.')
            x = len(fileArr)
            fileName = file.split('.' + fileArr[x-1])
            fileExt = '.' + fileArr[x-1]
            fileName = fileName[0]
            # checks images in transformed directory
            if not_exists(fileName, fileExt, transformstr):
                # multithread processing
                t = Thread(target=funcTrans, args=(rawDir, fileName, fileExt, flip, angle, options.expand, newWidth, newHeight, options.aspectratio, options.order, transformstr))
                t.start()  
    except:
        print(
            "\n The directory at: \n " + rawDir + "  \n does not exists")
# END OF MAIN

# Transformation function
def funcTrans(rawDir, fileName, fileExt, flip, angle, expand, newWidth, newHeight, ratio, order, transformstr):
    try:
        path = os.path.join(rawDir, fileName + fileExt)
        im = Image.open(path)
        for o in order:
            if(o == 's'):
                im = resizeFunc(im, newWidth, newHeight, ratio)
            if(o == 'f'):
                im = flipFunc(im, flip)
            if(o == 'r'):
                im = rotFunc(im, angle, expand)
        im.save(os.path.join(directory, fileName + transformstr + fileExt))   
    except:
        pass

# Resize image
def resizeFunc(im, newWidth, newHeight, ratio):
    width = im.size[0]
    height = im.size[1]
    try:
        # keeping the ratio
        if(ratio):
            # resize width
            if(newWidth == 0 and newHeight != 0):
                ar = newHeight / height
                size = [int(width * ar), newHeight]
                size = tuple(size)
                im = im.resize(size)
            # resize height keeping the ratio
            if(newWidth != 0):
                ar = newWidth / width
                size = [newWidth, int(height * ar)]
                size = tuple(size)
                im = im.resize(size)
        # not keeping the ratio        
        else:
            if(newWidth != 0 and newHeight != 0):
                size = [newWidth, newHeight]
                size = tuple(size)
                im = im.resize(size)
            if((newWidth == 0 or newHeight == 0) and not(newWidth == 0 and newHeight == 0)):
                size = [newWidth + width * (newWidth==0), newHeight + height * (newHeight==0)]
                size = tuple(size)
                im = im.resize(size)
        return im
    except:
        pass

# Flip image
def flipFunc(im, flip):
    try:
        if (flip[0] == 1):
            im = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        if (flip[1] == 1):
            im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        return im
    except:
        pass

# Rotate image
def rotFunc(im, angle, expand):
    try:
        if (angle != 0):
            im = im.rotate(angle, expand=expand)
        return im
    except:
        pass

# Checks for existing files
def not_exists(fileName, ext, transformstr):
    if os.path.isfile(os.path.join(directory, fileName + transformstr + ext)):
        screenLock.acquire()
        print("File " + fileName + transformstr + ext + " is already transformed!")
        screenLock.release()
        return False
    else:
        return True

if __name__ == '__main__':
    main()