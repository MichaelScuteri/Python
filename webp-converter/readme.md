# webp-converter.py
An easy and convenient way to convert a large number of image files to .webp format. webp-converter.py is much faster then any online converters or programs and is just as east to use.

The script utilises Google's libwebp package to convert the image files and allows for a lot of customization of how you want to convert them by simply editing one line in the python file.

# How to use?
The script only has one dependency, which is the libwebp package. You can download it [here](https://developers.google.com/speed/webp/docs/precompiled).

### Setting Up libwebp
Once you have downloaded the libwebp package either simply place it into the libwebp placeholder folder downloaded with this project or set it to your environment path.

Setting it to your environment PATH for current session:

    $env:PATH += ";C:\Path\To\libwebp\bin\cwebp.exe"

Set it permanently to your environment:

    [Environment]::SetEnvironmentVariable("PATH", $env:PATH + "C:\Path\To\libwebp\bin\cwebp.exe", [EnvironmentVariableTarget]::Machine)

### Converting Images

Place all images you want to convert into the empty /convert folder and run the python script.

The script will convert all your images to webp format and place them in a new directory called webp-files.

# Future Features

I am planning on continuing development on this project to include further features that are included in the libwebp library and making it easy to control from the command line.
- **dwebp:** Decompress a webp file to an image file
- **gif2webp:** Convert GIF to webp
- **img2ewebp:** Create animated WebP file from a sequence of input images.
- **vwebp:** Decompress a WebP file and display it in a window