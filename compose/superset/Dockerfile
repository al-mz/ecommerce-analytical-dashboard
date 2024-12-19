FROM apache/superset@sha256:51a90d11a59ac522172642cece4bd8047917253e13d884293fcd0cd48419939c

USER root

RUN pip install psycopg==3.1.18 gevent==24.10.3

COPY ./compose/superset/superset_init.sh /superset_init.sh

RUN chmod +x /superset_init.sh

USER superset

ENTRYPOINT [ "/superset_init.sh" ]