FROM debian:7
MAINTAINER Radu Ciorba raduciorba@gmail.com

RUN apt-get -qq update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python2.7 python-setuptools libzmq1 -y; easy_install pip
ADD ./src/ /var/www/src
ADD ./wheelhouse/ /var/www/wheelhouse
RUN pip install -r /var/www/src/REQUIREMENTS --no-index --find-links /var/www/wheelhouse; pip install -e /var/www/src/

USER www-data
CMD export TWIT_SETTINGS=/conf/twit.conf; export ES_URL=http://$ES_PORT_9200_TCP_ADDR:$ES_PORT_9200_TCP_PORT; supervisord -c /var/www/src/supervisor.conf
# assumes /var/log/twit exists and is writable; should be bind mounted from the host