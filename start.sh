#!/bin/bash

# On ajoute le répertoire courant au chemin de recherche de Python
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

# On lance Uvicorn en lui disant que l'app est dans src/main.py
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# On lance Streamlit
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0