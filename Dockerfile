FROM            base
MAINTAINER      isaccchoi@naver.com

ENV             LANG C.UTF-8

COPY            . /srv/app
RUN             /root/.pyenv/versions/app/bin/pip install -r \
                /srv/app/requirements.txt