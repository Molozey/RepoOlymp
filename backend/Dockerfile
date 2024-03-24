FROM python:3.12

RUN mkdir -p /backend

ENV PYTHONPATH='backend'

WORKDIR backend/
COPY req.txt .

RUN ls

RUN pip install -r req.txt

WORKDIR /
CMD ["python", "-m", "backend.run"]