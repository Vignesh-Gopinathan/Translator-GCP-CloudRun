#!/bin/bash

python download_model.py
streamlit run --server.headless=true --server.port=8080 app.py