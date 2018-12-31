import cv2

class Color():
    def __init__(self):
        pass

    def all_ans_to_bw(self, images):
        bw_images = []
        for img in images:
            bw_img = self.white_and_black(img)
            bw_images.append(bw_img)
        return bw_images

    #takes in an image (numpy array) and converts it to bw reversed
    def white_and_black(self, img_np):
        image_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        #convert image to black or white
        #determine the threshold automatically using the Otsu method,
        (threshold, image_bw) = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        #flip the color because our model had white numbers on a black background
        wb_image = (255-image_bw)

        return wb_image

    def black_and_white(self, img_np):
        image_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        #convert image to black or white
        #determine the threshold automatically using the Otsu method,
        (threshold, image_bw) = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return image_bw
