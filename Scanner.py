from TopDown import TopDown
from Color import Color
import cv2
import imutils
import numpy as np
from PIL import Image
import io

class Scanner():
    def __init__(self):
        pass

    def scan(self, file):
        pil_image = Image.open(io.BytesIO(file))
        image_np = np.array(pil_image)
        ratio = image_np.shape[0] / 500.0
        image_copy = image_np.copy()
        #convert to 32-bit floating point because of a bug with openCV 3
        image_np = imutils.resize(image_np, height=500)

        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        #find the contours in the edged image, keeping only the largest ones,
        #and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        #iterate over the contours
        for line in cnts:
            #approximate the contours
            peri = cv2.arcLength(line, True)
            approx = cv2.approxPolyDP(line, 0.02 * peri, True)

            if(len(approx) == 4):
                screen_cnt = approx
                break

        #apply the four point transform to obtain a top down
        #view of the original image
        top_down = TopDown()
        warped_img = top_down.four_point_transform(image_copy, screen_cnt.reshape(4, 2) * ratio)

        return warped_img #return the scanned doc with just the test, and a birds eye view perspective
