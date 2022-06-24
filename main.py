from sentence_transformers import SentenceTransformer, util
import os
from flask import Flask, jsonify, request
import torch

print('Loading model ...')
model_path = "./model"
model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2",
    cache_folder=model_path
)
print('Done loading ... ready for inference')

def new_cosine_similarity(source, target):
    #Compute embedding for both lists
    with torch.no_grad():
        embedding_1= model.encode(source, convert_to_tensor=True)
        embedding_2 = model.encode(target, convert_to_tensor=True)
        return util.pytorch_cos_sim(embedding_1, embedding_2).item()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "App is up and running!"

@app.route('/predictions', methods=['POST'])
def calculate_similarity():
    content = request.json
    print(f'Got request {content}')
    api_key = content.get('api_key')
    source = content.get('source')
    target = content.get('target')
    if source is None or target is None:
        return jsonify(code=403, message="bad request: source or target is missing")
    if  api_key != "FD0568E53F09CD0B8050B492B142F35A94DB7F4E241A217ACCC1B2B2A4FDB63B":
        return jsonify(code=403, message="bad request: bad api_key")
    print('Doing inference ...')
    similarity = new_cosine_similarity(source, target)
    return jsonify({"status":"success", "prediction":similarity})

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
