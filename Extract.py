import imutils
import cv2
from PIL import Image
import numpy as np
from TopDown import TopDown

class Extract():
    def __init__(self):
        pass

    def get_all_answers(self, image_np, num_questions):
        answers = []
        #takes in the scanned doc
        rough_cropped_answers = self.crop_answers(image_np, num_questions) #get a rough crop of all the answers

        for rough_ans in rough_cropped_answers:
            single_ans_img = self.get_answer(rough_ans)
            answers.append(single_ans_img)

        #remove black box from answer image
        best_answers = []
        shape = {
            "top": 10,
            "bottom": -10,
            "left": 10,
            "right": -10
        }
        for cropped_ans in answers:
            final_img = self.get_answer_hard(cropped_ans, shape)
            best_answers.append(final_img)

        return best_answers #returns a list of the answers as images (numpy arrays)

    #takes in a scanned image as a numpy array
    #return a list of the answers that have been cropped from the scanned doc as numpy arrays
    def crop_answers(self, image_np, num_questions):
        #convert from numpy array to Image so we can give it a new height and width
        #test document has about a 61 height: 50 width ratio, so we will always make it something like that

        pil_image = Image.fromarray(image_np, "RGB")
        pil_img_resized = pil_image.resize((1000, 1220), Image.ANTIALIAS)

        #now we need to crop a rough estimate of where all the answers are so we can pas it to get answer
        COLUMS = 5
        ROWS = 9

        # get section with just the answers
        LEFT = 138
        TOP = 153
        # these(below) can be looser because the cropping of each image with handle the extra space
        RIGHT = 780
        BOTTOM = 1090

        answers_rect = (LEFT, TOP, RIGHT, BOTTOM)
        image_ans_region = pil_img_resized.crop(answers_rect)

        ans_img_as_pil = []

        #answer_dimensions
        ans_height = 109
        ans_width = 115

        #keep a counter so we only grab the boxes that have answers
        question_num = 0

        #initialize first box right stuff
        ans_top = 0
        ans_bottom = ans_top+ans_height
        height_space = -8
        for row in range(0, ROWS):
            #initialize first box left stuff
            ans_left = 0
            ans_right = ans_left + ans_width
            width_space = 12
            for col in range(0, COLUMS):
                single_ans_rect = (ans_left, ans_top, ans_right, ans_bottom)
                single_ans_img = image_ans_region.crop(single_ans_rect)
                ans_img_as_pil.append(single_ans_img)
                question_num += 1
                ans_left += (ans_width + width_space)
                ans_right = ans_left + ans_width
                if(question_num >= num_questions):
                    break
            else:
                ans_top += (ans_height + height_space)
                ans_bottom = ans_top + ans_height
                continue
            break

        ans_img_as_np = []
        for img in ans_img_as_pil:
            ans_np = np.array(img)
            ans_resized = imutils.resize(ans_np, width=80)
            ans_img_as_np.append(ans_resized)

        # #now convert back to numpy array
        # image_np = np.array(answer)
        # resized = imutils.resize(image_np, width=500)
        # ratio = image_np.shape[0] / float(resized.shape[0])

        return ans_img_as_np

    #basically do what we did to scan the document
    def get_answer(self, image_np):
        #image_np: numpy array that makes up the image
        #resize it to a smaller factor so that the shapes can be approximated better
        resized = imutils.resize(image_np, width=100)
        image_copy = image_np.copy()
        ratio = image_np.shape[0] / float(resized.shape[0])

        #get outline of answer box
        edged = cv2.Canny(resized, 75, 200)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours
        screen_cnt = None
        for contour in cnts:
            # approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screen_cnt = approx
                break
        #if we were not able to find the answer box in the image, just return a hard crop of the image
        if(screen_cnt is None):
            shape = {
                "top": 20,
                "bottom": -20,
                "left": 20,
                "right": -20
            }
            return self.get_answer_hard(image_copy, shape)

        top_down = TopDown()
        scanned_ans = top_down.four_point_transform(image_copy, screen_cnt.reshape(4, 2) * ratio)

        return scanned_ans  #return the answer box from an image

    #hard code the crop, instead of using edge detection
    def get_answer_hard(self, image_np, shape):
        dim = (200, 200)
        resized = cv2.resize(image_np, dim, interpolation=cv2.INTER_NEAREST)
        crop_img = resized[shape["top"]:shape["bottom"], shape["left"]:shape["right"]]
        return crop_img
