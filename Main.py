from flask import Flask
from flask_restful import Api
from Answers import Answers
from Storage import Storage


app = Flask(__name__)
api = Api(app)


api.add_resource(Answers, '/')
api.add_resource(Storage, '/data')
if __name__ == '__main__':
    app.run(debug=True)
