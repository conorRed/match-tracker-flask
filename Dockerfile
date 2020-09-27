FROM python:3.5.5
ADD . /app
WORKDIR /app
RUN pip install -r requirement.txt
WORKDIR /app
CMD flask run

