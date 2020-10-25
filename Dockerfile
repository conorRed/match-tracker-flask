FROM python:3.8
RUN useradd -ms /bin/bash match-tracker
WORKDIR /home/match-tracker 
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY app app
COPY migrations migrations
COPY config/ config
COPY match-tracker.py config.py boot.sh seed_cli.py ./
RUN chmod +x boot.sh
ENV FLASK_APP match-tracker.py

RUN chown -R match-tracker:match-tracker ./
USER match-tracker

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]    
