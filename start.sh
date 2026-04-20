#!/bin/bash
# Lancer FastAPI en arrière-plan sur le port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &
# Lancer Streamlit sur le port 8501
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
