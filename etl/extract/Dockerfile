FROM python:3.11-slim-bullseye

WORKDIR /extract

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py"]