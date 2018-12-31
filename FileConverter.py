from io import BytesIO
from PIL import Image
import io
import numpy as np
from itertools import groupby




class FileConverter():
    def __init__(self):
        pass

    def png_to_jpeg(self, file):
        image_bytes = file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        orientation = self.get_orientation(pil_image)

        pil_image = self.fix_orientation(pil_image, orientation)

        pil_image = pil_image.convert("RGB") #remove alpha channel from png because jpeg doesnt support it
        with BytesIO() as image:
            pil_image.save(image, format="JPEG")
            return image.getvalue()

    def get_orientation(self, pil_image):
        if (hasattr(pil_image, "_getexif")):
            exifdata = pil_image._getexif()
            try:
                orientation = exifdata.get(274)
            except:
                #there was no exif data
                orientation = 1
        else:
            orientation = 1
        return orientation

    def fix_orientation(self, img, orientation):
        if orientation is 1:  # Horizontal (normal)
            pass
        elif orientation is 2:  # Mirrored horizontal
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 3:  # Rotated 180
            img = img.rotate(180)
        elif orientation is 4:  # Mirrored vertical
            img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 5:  # Mirrored horizontal then rotated 90 CCW
            img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 6:  # Rotated 90 CCW
            img = img.rotate(-90)
        elif orientation is 7:  # Mirrored horizontal then rotated 90 CW
            img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 8:  # Rotated 90 CW
            img = img.rotate(90)
        return img

    def image_to_numpy(self, image):
        return np.array(image)

    def convert_images(self, list_of_images):
        out_list = []
        for img in list_of_images:
            temp_img = self.convert_image(img)
            out_list.append(temp_img)
        return out_list

    #take in the image (like (28, 28))
    def convert_image(self, image_np):
        #one_layer_img = image_np[:, :, 0] # the array looks like (28,28, 3) and this makes it (28, 28)
        # now it needs to look like (1, 28, 28, 1) (because of the data we trained on)
        flat_img = image_np.flatten()
        shaped_img = flat_img.reshape(1, 28, 28, 1).astype("float32")
        return shaped_img

    def get_string_images(self, images):
        str_images = []
        for img in images:
            str_images.append(self.get_string_image(img))
        return str_images

    def get_string_image(self, image_2d):
        image_1d = image_2d[0].reshape(784).astype('float32')
        image_1d[image_1d > 128] = 1  #make this binary
        image_str = ''.join(str(int(x)) for x in image_1d)
        return image_str

    def compress_images(self, images):
        compressed_strings = []
        for img in images:
            compressed_strings.append(self.compressor(img))
        return compressed_strings

    def compressor(self, pixels):
        pixels = pixels.replace('0', 'F')
        pixels = pixels.replace('1', 'T')

        groups = groupby(pixels)
        result = [(label, sum(1 for x in group)) for label, group in groups]
        compressed_str = ''.join('{}{}'.format(label, count) for label, count in result)

        return compressed_str

