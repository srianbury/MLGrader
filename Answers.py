from FileConverter import FileConverter
from Scanner import Scanner
from Extract import Extract
from Color import Color
from Size import Size
from ModelLoader import ModelLoader
from keras.optimizers import RMSprop
from Grader import Grader
from Storage import Storage
from flask_restful import Resource
from flask import request


class Answers(Resource):
    def get(self):
        storage = Storage()
        data = storage.read()
        return data, 200

    def post(self):
        req_img = request.files['image']
        answers = self.process_image(req_img)
        return {'answers': answers}, 200

    def process_image(self, image):
        file_converter = FileConverter()
        #convert the image to byte string
        image_bytes = file_converter.png_to_jpeg(image)

        scanner = Scanner()
        #scan the image and give it a birds eye view, returns a np of pixels that makes up the image
        scan_np = scanner.scan(image_bytes)

        #extract the individual answers from the scanned test
        extractor = Extract()
        answers = extractor.get_all_answers(scan_np, 5)

        color = Color()
        bw_answers = color.all_ans_to_bw(answers)

        size = Size()
        DIM = (28, 28)
        shrunk_images = size.shrink_images(bw_answers, DIM)

        #convert the answer images to a single array, which we used in training our model
        answers_flat = file_converter.convert_images(shrunk_images)  #returns image as (1, 28, 28, 1) and as type float

        #now that we have a list of images of the answers as bw 1D numpy arrays,
        # we can run them through our model and grade them
        # first we need to load our model
        model_loader = ModelLoader()
        MODEL_JSON = 'models/modified_model_98.json'
        MODEL_WEIGHTS = 'models/modified_model_98.h5'
        model = model_loader.load_model_2(MODEL_JSON, MODEL_WEIGHTS)
        #compile model
        model.compile(optimizer=RMSprop(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

        grader = Grader()
        answers = grader.get_answers(answers_flat, model)

        #get the images as a 784 (28x28) length string so we can store the data in a database
        ans_strings = file_converter.get_string_images(answers_flat)
        compressed_images = file_converter.compress_images(ans_strings)

        #add the images to database so we can create a large dataset of handwritten letters
        # storage = Storage()
        # storage.insert(answers, compressed_images)

        return answers
