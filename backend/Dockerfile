FROM python:3.12

RUN mkdir -p /app
WORKDIR app/
COPY req.txt .

RUN ls

RUN pip install -r req.txt

CMD ["ls"]