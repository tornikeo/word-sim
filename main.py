# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_helloworld_service]
# [START run_helloworld_service]
from json import load
import os
from flask import Flask, jsonify, request
import torch
from sentence_transformers import SentenceTransformer, util
from functools import lru_cache

app = Flask(__name__)

@lru_cache(None)
def load_model():
    print('Loading model ...')
    model = SentenceTransformer(
        "sentence-transformers/distiluse-base-multilingual-cased-v2",
        cache_folder='./model'
    )
    print('Done loading ... ready for inference')
    return model

@lru_cache(2000)
def new_cosine_similarity(source, target):
    #Compute embedding for both lists
    model = load_model()
    with torch.no_grad():
        embedding_1= model.encode(source, convert_to_tensor=True)
        embedding_2 = model.encode(target, convert_to_tensor=True)
        return util.pytorch_cos_sim(embedding_1, embedding_2).item()

@app.route('/', methods=['GET'])
def hello():
    return "App is up and running!"

@app.route('/predictions', methods=['POST'])
def calculate_similarity():
    content = request.json
    print(f'Got request {content}')
    source = content.get('source')
    target = content.get('target')
    if source is None or target is None:
        return jsonify(code=403, message="bad request: source or target is missing")
    print('Doing inference ...')
    similarity = new_cosine_similarity(source, target)
    return jsonify({"status":"success", "prediction":similarity})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
