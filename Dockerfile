FROM python:3-alpine
MAINTAINER James <james@nurture.ai>

RUN apk update \
  &&  apk add ca-certificates wget \
  && update-ca-certificates

RUN pip --version
RUN pip install arxivscraper

RUN adduser -h /home/app -D -s /bin/bash -g app,sudo app
#RUN usermod -a -G app,sudo app

RUN mkdir -p /home/app/.ssh
RUN mkdir -p /home/app/bin
RUN chown -R app:app /home/app

ENV LANG en_US.utf8
ENV SSH_KEY ""
ENV SSH_KEY2 ""

WORKDIR /home/app

EXPOSE 5005
WORKDIR /home/app

COPY docker-entrypoint.sh /home/app/bin/
RUN chmod a+x /home/app/bin/docker-entrypoint.sh
COPY scraper.py /home/app/bin/

# ==========================================
# finalize

ENTRYPOINT ["/home/app/bin/docker-entrypoint.sh"]
