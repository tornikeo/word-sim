from sentence_transformers import SentenceTransformer

print('Loading model ...')
model_path = "./model"
model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2",
    cache_folder=model_path
)
print('Done loading ... ready for inference')