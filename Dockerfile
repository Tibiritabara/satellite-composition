FROM python:3.7

ENV PORT 8080
ENV DEBUG "True"
ENV LOCAL_STORAGE "cache/"
ENV REMOTE_STORAGE "https://storage.googleapis.com/interstellar-backend-challenge/"
ENV GENERATION_STORAGE "cache/generated/"
#RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update
RUN apt-get install -y python python-pip python-dev python-numpy gdal-bin libgdal-dev
RUN pip install pipenv
ADD . /app
WORKDIR /app
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE $PORT

CMD gunicorn -b :$PORT interstellar.wsgi
