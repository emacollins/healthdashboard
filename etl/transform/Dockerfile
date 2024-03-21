FROM python:3.11-slim-bullseye

WORKDIR /healthdashboard/etl/transform

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py"]