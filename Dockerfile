FROM python:3.5.5
ADD . /app
WORKDIR /app
RUN pip install -r requirement.txt
WORKDIR /app
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

