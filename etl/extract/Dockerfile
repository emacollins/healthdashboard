FROM python:3.11-slim-bullseye

WORKDIR /healthdashboard/etl/extract

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "run.py"]