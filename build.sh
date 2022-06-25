#!/bin/bash
docker build -t gcr.io/news-languages/word-sim:latest . 
docker run -it --rm -p 8080:9090 -e PORT=9090 gcr.io/news-languages/word-sim:latest