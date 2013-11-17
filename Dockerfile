FROM ubuntu:12.04
RUN apt-get update -q
RUN apt-get install -qy python-setuptools git build-essential python-dev
RUN easy_install pip
#RUN pip install Cython
#RUN pip install git+git://github.com/surfly/gevent.git
RUN pip install http://builds.enix.org/napix/permissions-latest.tar.gz
RUN pip install http://builds.enix.org/napix/napix-latest.tar.gz
RUN pip install http://builds.enix.org/napix/napixd-latest.tar.gz
RUN pip install http://builds.enix.org/napix/NapixCLI-latest.tar.gz
RUN pip install pyinotify
RUN pip install git+git://github.com/dotcloud/docker-py.git
EXPOSE 8002
ENV NAPIXHOME /napix
VOLUME /napix/auto
ADD wrapper /wrapper
ENTRYPOINT /wrapper
