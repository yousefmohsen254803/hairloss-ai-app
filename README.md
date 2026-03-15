# Hair Loss AI App

This project contains a Streamlit frontend and a FastAPI backend for hair loss classification using a TensorFlow model.

## Requirements
- Docker
- Docker Compose

## Run the application

From the project folder run:

docker compose up --build

Then open the app in your browser:

http://localhost:8501

## Services

Streamlit frontend  
Port: 8501

FastAPI prediction API  
Port: 8000

## API Endpoint

POST /predict

Upload an image file to receive a prediction.

## Stop the application

Press:

Ctrl + C