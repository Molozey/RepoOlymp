FROM python:3.12

RUN mkdir -p /frontend
WORKDIR frontend/

ENV PYTHONPATH='frontend'


COPY req.txt .

RUN pip install -r req.txt

WORKDIR /frontend/app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]