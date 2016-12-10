FROM python:3.5
ENV PYTHONUNBUFFERED 1

MAINTAINER Carl Lewis (carl@streamsavvy.tv)

ENV DEBIAN_FRONTEND noninteractive
####################################################
# OS Updates and Python packages
####################################################
RUN apt-get update\
&& apt-get upgrade -y\
&& apt-get install -y
RUN apt-get install -y apt-utils

# Libs required for geospatial libraries on Debian...
RUN apt-get -y install binutils libproj-dev gdal-bin

####################################################
# A Few pip installs not commonly in requirements.txt
####################################################
RUN apt-get install -y nano wget
# build dependencies for postgres and image bindings
RUN apt-get install -y --no-install-recommends python-imaging python-psycopg2 postgresql-client

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
#expose listen ports
EXPOSE 80

CMD ["gunicorn", "streamsavvy_dataprocessing.wsgi"]