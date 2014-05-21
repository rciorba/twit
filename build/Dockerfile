FROM debian:7.4
MAINTAINER Radu Ciorba raduciorba@gmail.com

RUN apt-get -qq update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python2.7 python-setuptools -y; easy_install pip
ADD ./src/ /var/www/src
ADD ./wheelhouse/ /var/www/wheelhouse
RUN pip install -r /var/www/src/REQUIREMENTS --no-index --find-links /var/www/wheelhouse; pip install -e /var/www/src/

USER www-data
CMD supervisord -c /var/www/src/supervisor.conf
# assumes /var/log/twit exists and is writable; should be bind mounted from the host