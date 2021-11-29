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
 git clone https://github.com/Kaszabi/Python-Image-Editor-Script.git
``` 
### Converter usage
```python
 python convert.py <options>
 
 # Options listed below


```

### Example usage

```
 git clone https://github.com/Kaszabi/Python-Image-Editor-Script.git
 cd [my-app-name]
 cd app
 
 # simple usage
 python convert.py --s <Enter-Path-Of-Directory>
 # set a custom target image format
 python convert.py --s <Enter-Path-Of-Directory> --ext '.png'
```
- The --s argument is where you set the path to the directory you want to convert! 
- The --ext argument is where you specify the image format that will be used for the converted images; by default the `.jpg` is used. valid options are:
    - `.jpg`
    - `.png`

The application will create a folder 'converted' where all your converted images are located!

And you are done! 

## ScreenShot
<img src='sample.png' alt='Python Image Converter'>
