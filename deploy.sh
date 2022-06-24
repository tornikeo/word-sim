#!/bin/bash
docker build -t gcr.io/news-languages/word-sim:latest . 
gcloud builds submit \
    --tag gcr.io/news-languages/word-sim:latest \
    --machine-type=n1-highcpu-8
gcloud run deploy word-sim \
    --image gcr.io/news-languages/word-sim:latest \
    --cpu=2 \
    --memory=8Gi \
    --allow-unauthenticated \
    --region=us-east1 \
    --port=8080 \
    --min-instances=1 