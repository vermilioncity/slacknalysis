FROM python:3.9

WORKDIR superset

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade --no-cache-dir setuptools pip \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY docker-init.sh .
COPY docker-entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]

EXPOSE 8088