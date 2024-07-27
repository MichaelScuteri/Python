import os
import sys
import subprocess
import shutil

out_dir = "webp-files"
input_dir = "./convert"
extensions = (".png", ".jpg", ".jpeg", ".tiff")
images = []
script_dir = os.path.dirname(os.path.realpath(__file__))
libwebp = os.path.join(script_dir, "libwebp", "libwebp-1.4.0", "bin", "cwebp.exe")

def find_image_dir():
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(extensions):
                images.append(file)
    return images

def convert(images):
    for image in images:
        print(f"Conerting {image}...")
        input_file = os.path.join(input_dir, image)
        output_file = os.path.join(out_dir, os.path.splitext(image)[0] + ".webp")
        subprocess.run([libwebp, "-quiet", "-q", "80", input_file, "-o", output_file])

def main():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        find_image_dir()
    else:
        find_image_dir()

    convert(images)
    print(f"Converted {len(images)} image(s) to WebP format.")
    
main()


