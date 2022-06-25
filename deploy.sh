#!/bin/bash
gcloud builds submit \
    --tag gcr.io/news-languages/word-sim \
    --machine-type=n1-highcpu-8
gcloud run deploy word-sim \
    --image gcr.io/news-languages/word-sim \
    --cpu=4 \
    --memory=16Gi \
    --no-allow-unauthenticated \
    --region=us-east1 \
    --min-instances=1