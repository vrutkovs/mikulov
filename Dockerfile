FROM fedora:26

RUN dnf update -y --refresh && \
    dnf install -y git npm && \
    dnf clean all

ADD . /mikulov

ARG DEBUG

RUN cd /mikulov && \
    npm install patternfly@3.25.1 --save --prefix=mikulov/static && \
    pip3 install -r requirements.txt && \
    if [ -n $DEBUG ]; then pip3 install -r requirements_dev.txt; fi && \
    git log -1 --pretty=format:'%h' --abbrev-commit > mikulov/templates/commit.jinja2

WORKDIR /mikulov/mikulov

EXPOSE 8080

CMD ["python3", "server.py"]
