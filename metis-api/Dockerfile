FROM python:3.9


WORKDIR /app


COPY ./requirements.txt ./requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /app

EXPOSE 80

CMD ["python", "main.py"]