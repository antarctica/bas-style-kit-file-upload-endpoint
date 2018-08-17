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

# Add application - more complicated because COPY only copies the contents of a directory for some insane reason
COPY file_upload_endpoint/ /usr/src/app/file_upload_endpoint/
COPY config.py manage.py /usr/src/app/

# Setup runtime
ENTRYPOINT []
CMD flask run --host 0.0.0.0 --port $PORT

RUN echo "python version: " && python --version && \
    echo "pip version: " && pip --version
