#!/bin/sh
python3 src/main.py /toy-static-site-generator/ && \
cd docs && python3 -m http.server 8888
