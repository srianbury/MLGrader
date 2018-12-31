from keras.models import model_from_json
from keras.optimizers import RMSprop

class ModelLoader():
    def __init__(self):
        pass

    #import the model from json file and return it
    def load_model(self, json_file, weights):
        with open(json_file, "r") as file:
            json_string = file.read()
            model = model_from_json(json_string)
            model.load_weights(weights)
            return model

    def load_model_2(self, model_json, model_weights):
        json_file = open(model_json, "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(model_weights)
        return loaded_model

    def compile_model(self, model):
        return model.compile(optimizer=RMSprop(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
