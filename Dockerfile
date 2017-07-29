FROM fedora:26

ARG DEBUG
RUN dnf update -y --refresh && \
    dnf install -y git npm && \
    if [ -n $DEBUG ]; then dnf install -y python3-aiohttp python3-jinja2 python3-flake8 python3-ipdb python3-aiofiles && pip3 install aiohttp-jinja2; fi && \
    dnf clean all

ADD . /mikulov

RUN cd /mikulov && \
    npm install --save-dev tachyons@4.7.0 --prefix=mikulov/static && \
    pip3 install -r requirements.txt && \
    git log -1 --pretty=format:'%h' --abbrev-commit > mikulov/templates/commit.jinja2

WORKDIR /mikulov/mikulov

EXPOSE 8080

CMD ["python3", "server.py"]
