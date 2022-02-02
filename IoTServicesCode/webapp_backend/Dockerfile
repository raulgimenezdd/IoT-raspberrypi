FROM python:3.7.3

COPY /app /etc/usr/src/app

WORKDIR /etc/usr/src/app

RUN pip install mysql-connector-python Flask Flask-Cors PyYAML requests

ENTRYPOINT ["python"]

CMD ["webapp_rest_api.py"]