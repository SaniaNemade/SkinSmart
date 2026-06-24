import os
from typing import List
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from models.skin_tone.skin_tone_knn import identify_skin_tone
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import werkzeug
from models.recommender.rec import recs_essentials, makeup_recommendation, generate_analysis_graphs
import base64
from io import BytesIO
from PIL import Image
import tf_keras as k3

app = Flask(__name__)
api = Api(app)

class_names1 = ['Dry_skin', 'Normal_skin', 'Oil_skin']
class_names2 = ['Low', 'Moderate', 'Severe']
skin_tone_dataset = 'models/skin_tone/skin_tone_dataset.csv'


def get_model():
    global model1, model2
    model1 = k3.models.load_model('./models/skin_model')
    print('Model 1 loaded')
    model2 = k3.models.load_model('./models/acne_model')
    print("Model 2 loaded!")


def load_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    return img_tensor


def prediction_skin(img_path):
    new_image = load_image(img_path)
    pred1 = model1.predict(new_image)
    if len(pred1[0]) > 1:
        pred_class1 = class_names1[tf.argmax(pred1[0])]
    else:
        pred_class1 = class_names1[int(tf.round(pred1[0]))]
    return pred_class1


def prediction_acne(img_path):
    new_image = load_image(img_path)
    pred2 = model2.predict(new_image)
    if len(pred2[0]) > 1:
        pred_class2 = class_names2[tf.argmax(pred2[0])]
    else:
        pred_class2 = class_names2[int(tf.round(pred2[0]))]
    return pred_class2


get_model()


img_put_args = reqparse.RequestParser()
img_put_args.add_argument(
    "file", help="Please provide a valid image file", required=True)


rec_args = reqparse.RequestParser()

rec_args.add_argument(
    "tone", type=int, help="Argument required", required=True)
rec_args.add_argument(
    "type", type=str, help="Argument required", required=True)
rec_args.add_argument("features", type=dict,
                      help="Argument required", required=True)
# Add optional weight parameters
rec_args.add_argument("weights", type=dict, required=False, default=None)
rec_args.add_argument("price_range", type=str, required=False, default=None)


class Recommendation(Resource):
    def put(self):
        args = rec_args.parse_args()
        print(args)
        features = args['features']
        tone = args['tone']
        skin_type = args['type'].lower()
        skin_tone = 'light to medium'
        if tone <= 2:
            skin_tone = 'fair to light'
        elif tone >= 4:
            skin_tone = 'medium to dark'
        print(f"{skin_tone}, {skin_type}")
        
        # Extract weights from features if they exist there
        weight_skin = features.pop('weight_skin', None)
        weight_acne = features.pop('weight_acne', None)
        weight_price = features.pop('weight_price', None)
        
        # Build feature vector (only the actual features, not weights)
        fv = []
        for key, value in features.items():
            fv.append(int(value))
        
        # Get weights from args or from features
        weights = args.get('weights')
        price_range = args.get('price_range')
        
        # If weights not in args, check if they were in features
        if weights is None and weight_skin is not None:
            # Normalize weights to 0-1 range (assuming they come as 1-5 scale)
            weights = {
                'skin': float(weight_skin) / 5.0,
                'acne': float(weight_acne) / 5.0,
                'price': float(weight_price) / 5.0
            }
        elif weights is None:
            # Use defaults
            weights = {'skin': 0.5, 'acne': 0.5, 'price': 0.5}
        else:
            # Ensure all weight keys exist
            weights = {
                'skin': float(weights.get('skin', 0.5)),
                'acne': float(weights.get('acne', 0.5)),
                'price': float(weights.get('price', 0.5))
            }
        
        print(f"Received weights: {weights}")
        print(f"Price range: {price_range}")
        
        # Generate recommendations
        general = recs_essentials(fv, None, weights=weights, price_range=price_range)
        makeup = makeup_recommendation(skin_tone, skin_type)
        
        # Generate analysis graphs
        graphs = generate_analysis_graphs(fv, weights=weights, price_range=price_range)
        
        return {
            'general': general, 
            'makeup': makeup,
            'graphs': graphs
        }


class SkinMetrics(Resource):
    def put(self):
        args = img_put_args.parse_args()
        print()
        print(args)
        print()
        file = args['file']
        starter = file.find(',')
        image_data = file[starter+1:]
        print()
        print(image_data)
        print()
        image_data = bytes(image_data, encoding="ascii")
        im = Image.open(BytesIO(base64.b64decode(image_data+b'==')))

        filename = 'image.png'
        file_path = os.path.join('./static', filename)
        im.save(file_path)
        skin_type = prediction_skin(file_path).split('_')[0]
        acne_type = prediction_acne(file_path)
        tone = identify_skin_tone(file_path, dataset=skin_tone_dataset)
        print(skin_type)
        print(acne_type)
        print(tone)

        return {'type': skin_type, 'tone': str(tone), 'acne': acne_type}, 200


api.add_resource(SkinMetrics, "/upload")
api.add_resource(Recommendation, "/recommend")

if __name__ == "__main__":
    app.run(debug=False)