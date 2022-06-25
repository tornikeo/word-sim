from sentence_transformers import SentenceTransformer, util

print('Loading and caching the model')
SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2",
    cache_folder='./model'
)
print('Loading model done')
