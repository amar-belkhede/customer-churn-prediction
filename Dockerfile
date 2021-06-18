FROM ubuntu

Label Amarkumar Belkhede "belkhedeamar@gmail.com"

WORKDIR /app

RUN apt-get -y update &&\
    apt-get -y install python3 python3-pip

RUN python3 -m pip install --upgrade pip



ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

ADD churnprediction churnprediction
ADD run.py .

RUN python3 -u ./churnprediction/ml_model.py

CMD [ "python3", "-u", "./run.py", "-e", "production" ]
EXPOSE 5000