from flask import Flask, render_template, request
# from flask.templating import render_template_string
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import cv2 as cv
import os

app = Flask(__name__)

breeds = ['boston_bull', 'dingo', 'pekinese', 'bluetick', 'golden_retriever',
       'bedlington_terrier', 'borzoi', 'basenji', 'scottish_deerhound',
       'shetland_sheepdog', 'walker_hound', 'maltese_dog',
       'norfolk_terrier', 'african_hunting_dog',
       'wire-haired_fox_terrier', 'redbone', 'lakeland_terrier', 'boxer',
       'doberman', 'otterhound', 'standard_schnauzer',
       'irish_water_spaniel', 'black-and-tan_coonhound', 'cairn',
       'affenpinscher', 'labrador_retriever', 'ibizan_hound',
       'english_setter', 'weimaraner', 'giant_schnauzer', 'groenendael',
       'dhole', 'toy_poodle', 'border_terrier', 'tibetan_terrier',
       'norwegian_elkhound', 'shih-tzu', 'irish_terrier', 'kuvasz',
       'german_shepherd', 'greater_swiss_mountain_dog', 'basset',
       'australian_terrier', 'schipperke', 'rhodesian_ridgeback',
       'irish_setter', 'appenzeller', 'bloodhound', 'samoyed',
       'miniature_schnauzer', 'brittany_spaniel', 'kelpie', 'papillon',
       'border_collie', 'entlebucher', 'collie', 'malamute',
       'welsh_springer_spaniel', 'chihuahua', 'saluki', 'pug', 'malinois',
       'komondor', 'airedale', 'leonberg', 'mexican_hairless',
       'bull_mastiff', 'bernese_mountain_dog',
       'american_staffordshire_terrier', 'lhasa', 'cardigan',
       'italian_greyhound', 'clumber', 'scotch_terrier', 'afghan_hound',
       'old_english_sheepdog', 'saint_bernard', 'miniature_pinscher',
       'eskimo_dog', 'irish_wolfhound', 'brabancon_griffon',
       'toy_terrier', 'chow', 'flat-coated_retriever', 'norwich_terrier',
       'soft-coated_wheaten_terrier', 'staffordshire_bullterrier',
       'english_foxhound', 'gordon_setter', 'siberian_husky',
       'newfoundland', 'briard', 'chesapeake_bay_retriever',
       'dandie_dinmont', 'great_pyrenees', 'beagle', 'vizsla',
       'west_highland_white_terrier', 'kerry_blue_terrier', 'whippet',
       'sealyham_terrier', 'standard_poodle', 'keeshond',
       'japanese_spaniel', 'miniature_poodle', 'pomeranian',
       'curly-coated_retriever', 'yorkshire_terrier', 'pembroke',
       'great_dane', 'blenheim_spaniel', 'silky_terrier',
       'sussex_spaniel', 'german_short-haired_pointer', 'french_bulldog',
       'bouvier_des_flandres', 'tibetan_mastiff', 'english_springer',
       'cocker_spaniel', 'rottweiler']

@app.route('/')
def upload_file():
    return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        # filename = secure_filename(f.filename)
        filename = os.path.join(f.filename)
        f.save(filename)
        img = cv.imread(filename)
        # print(img)
        if type(img) == type(None):
            result = ' Invalid Image \n Image Shape = ' + str(img)
        else:
            img = cv.resize(img, (100,100))
            img = img.reshape(-1, 100, 100, 3)
            model = load_model('dogbreedmodelresnet50.h5')
            breedDetected = breeds[np.argmax(model.predict(img))]
            prediction = str(model.predict(img))
            accuracy = str(np.amax((model.predict(img))))
            result = 'Breed Detected = ' + breedDetected + '<br>' + 'Accuracy = ' + accuracy + '<br>' + 'Prediction = ' + prediction
    return render_template('index.html', result = result)
		
if __name__ == '__main__':
    app.run(debug = True)