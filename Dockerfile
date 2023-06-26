FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install pipenv

WORKDIR /app


COPY starter.py .

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

CMD ["python", "starter.py",  "2022", "4"]






