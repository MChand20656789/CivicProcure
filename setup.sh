#!/bin/bash

python -m pip install --upgrade pip

python -m pip install numpy==1.26.4 pandas==2.2.3 plotly==7.1.0

python -m pip install --no-deps streamlit==1.64.0

python -m pip install \
  "altair>=5,<7" \
  "anyio>=4,<5" \
  "click>=7,<9" \
  "httptools>=0.6.3,<1" \
  "itsdangerous>=2.1,<3" \
  "pillow>=7.1,<13" \
  "protobuf>=5.26.1,<8" \
  "pydeck>=0.8.0b4,<1" \
  "python-multipart>=0.0.10,<1" \
  "requests>=2.27,<3" \
  "starlette>=0.46,<2" \
  "toml>=0.10.1,<2" \
  "typing-extensions>=4.10,<5" \
  "uvicorn>=0.30,<1" \
  "websockets>=12,<17"