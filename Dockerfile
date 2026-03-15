FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
EXPOSE 8000

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]