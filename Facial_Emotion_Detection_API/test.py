from flask import Flask,request,jsonify,Response
from flask_restful import Resource,Api
from PIL import Image,ImageFile
import cv2
import numpy
from demo import demo
from model import train_model, valid_model
import tensorflow as tf
import json
import sys
import base64


app = Flask(__name__)
api = Api(app)


flags =  tf.app.flags
flags.DEFINE_string('MODE', 'demo', 
                    'Set program to run in different mode, include train, valid and demo.')
flags.DEFINE_string('checkpoint_dir', './ckpt', 
                    'Path to model file.')
flags.DEFINE_string('train_data', './data/fer2013/fer2013.csv',
                    'Path to training data.')
flags.DEFINE_string('valid_data', './valid_sets/',
                    'Path to training data.')
flags.DEFINE_boolean('show_box', False, 
                    'If true, the results will show detection box')
FLAGS = flags.FLAGS

SAMPLE_IMAGE_PATH=""

class Image_Emotion_Recognition(Resource):
    assert FLAGS.MODE in ('train', 'valid', 'demo')
    def get(self):
        return {"about":'abc'}
    
    def post(self):
        
        x=""
        self.bytes_to_img(request.form['img'])
        if FLAGS.MODE == 'demo':
               img = Image.open('temp_file.jpg')
               open_cv_image = numpy.array(img) 
               open_cv_image = open_cv_image[:, :, ::-1].copy() 
               x=demo(FLAGS.checkpoint_dir, FLAGS.show_box,open_cv_image)
               print("test: = "+str(x))
        elif FLAGS.MODE == 'train':
               train_model(FLAGS.train_data)
        elif FLAGS.MODE == 'valid':
               valid_model(FLAGS.checkpoint_dir, FLAGS.valid_data)


        return json.loads(x)
    
    def image_to_bytes(self,url):
        with open("temp_file.jpg", "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
            return str
    
    def bytes_to_img(self,bytes):
        imgdata = base64.b64decode(bytes)
        filename = 'temp_file.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print('DONE')


class Multi(Resource):
    def get(self,num):
        return {'result':num*10}

api.add_resource(Image_Emotion_Recognition,'/Img_Emotion/')
api.add_resource(Multi,'/multi/<int:num>')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


