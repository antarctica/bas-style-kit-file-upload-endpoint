FROM python:3.6-alpine

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

# Setup project
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app
ENV FLASK_APP manage.py
ENV FLASK_ENV development

# Setup project dependencies
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Setup runtime
ENTRYPOINT []

RUN echo "python version: " && python --version && \
    echo "pip version: " && pip --version
