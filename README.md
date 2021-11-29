# Python-Image-Editor-Script

## Image editor/converter Python script for an assignment
The app is using PIL for image editing/converting. 

# What can you do with it ?
### Convert .tif, .tiff, .bmp, .jpg, .png, .jpeg files
You can only convert from/to these image extensions.

### You can also rotate, flip, and resize images
The script uses multithread and checks already existing images!

# Documentation

### Install Pillow package
```python
 pip install Pillow
```

### Clone git repository
```
 git clone https://github.com/Kaszabi/Python-Image-Editor-Script.git [Folder Name]
``` 
### Converter Usage
```python
 python app/convert.py <options>
 
 # Options listed below
 -d/--dest <folder destination> - the images in this folder will be converted and placed in the folder ./converted
 -r/--rext <raw extension> - only convert these image files('all', '.tif', '.tiff', '.bmp', '.jpg', '.png', '.jpeg')
 -t/--text <target extension> - convert to this extension('.tif', '.tiff', '.bmp', '.jpg', '.png', '.jpeg')
 
 # Example
 python app/convert.py -d <Path/Directory> -r 'all' -t '.png' # This will convert all image files to .png 
```
### Editor Usage
```python
 python app/transform.py <options>
 
 # Options listed below
 -d/--dir <folder destination> - # the images in this folder will be transformed and placed in the folder ./transformed
 -r/--rright <rotate right> - # (float) default=0
 -l/--rleft <rotate left> - # (float) default=0
 -e/--expand - # expands the output image to make it large enough to hold the entire rotated image
 -v/--fvert - # flip vertical
 -f/--fhor - # flip horizontal
 -W/--width <new width> - # (int)
 -H/--height <new height> - # (int) 
 -a/--aratio - # keep aspect ratio 
 -o/--order <new order> - # change the order of transformation tasks (s=size, f=flip, r=rotate) default='sfr'
                          # you can use the same transformations multiple times too, the script will do those tasks 
                          # multiple times
 
 # Examples
 python app/transform.py -d <Path/Directory> -r 180 -f -W 1920 -a # This will rotate the images by 180 degrees to 
                                                                  # the right, then flips them horizontally, and then
                                                                  # resizing them to the width 1920px while keeping 
                                                                  # all images own aspect ratio

 python app/transform.py -d <Path/Directory> -l 400 -f -o rrrrrrrrrff # This will rotate the images 9 times to the 
                                                                      # left by 40 degrees and then flips them horizontally
                                                                      # 2 times
```
## ScreenShots
<img src='sample.png' alt='Python Image Converter'>
