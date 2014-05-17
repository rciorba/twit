FROM debian:7.4
MAINTAINER Radu Ciorba raduciorba@gmail.com

RUN apt-get -qq update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python2.7 python-setuptools -y; easy_install pip
ADD ./src/ /var/www/src
ADD ./wheelhouse/ /var/www/wheelhouse
RUN pip install -r /var/www/src/REQUIREMENTS --no-index --find-links /var/www/wheelhouse
USER www-data