import cv2

class Size():
    def __init__(self):
        pass

    def shrink_images(self, images, dim):
        shrunk_images = []
        for img in images:
            shrnk_img = self.shrink(img, dim)
            shrunk_images.append(shrnk_img)
        return shrunk_images

    def shrink(self, image, dim):
        return cv2.resize(image, dim, interpolation=cv2.INTER_NEAREST)
