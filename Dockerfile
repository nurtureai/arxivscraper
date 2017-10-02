FROM python:3-alpine
MAINTAINER James <james@nurture.ai>

RUN apk update \
  &&  apk add ca-certificates wget git build-base\
  && update-ca-certificates

#RUN pip3 --version
#RUN pip3 install arxivscraper
RUN pip3 install gevent gunicorn flask

RUN adduser -h /home/app -D -s /bin/bash -g app,sudo app
#RUN usermod -a -G app,sudo app

RUN mkdir -p /home/app/.ssh
RUN mkdir -p /home/app/bin
RUN chown -R app:app /home/app

COPY arxivscraper.py /home/app/
COPY gunicorn.ini /home/app/
COPY server.py /home/app/
COPY config.py /home/app/
#RUN cd /home/app && git clone https://github.com/Mahdisadjadi/arxivscraper.git && cd arxivscraper && python setup.py install

ENV LANG en_US.utf8
ENV SSH_KEY ""
ENV SSH_KEY2 ""

WORKDIR /home/app
EXPOSE 5005

COPY docker-entrypoint.sh /home/app/bin/
RUN chmod a+x /home/app/bin/docker-entrypoint.sh
COPY scraper.py /home/app/bin/

# ==========================================
# finalize

ENTRYPOINT ["/home/app/bin/docker-entrypoint.sh"]
