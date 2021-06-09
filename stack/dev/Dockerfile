FROM ubuntu:latest

# install dev tools
RUN apt update && apt install -y \
    build-essential \
    bash-completion \
    wget \
    curl \
    nano \
    sudo \
    git \
    sqlite3 \
    python3 \
    python3-pip

# tell python not to write bytecode and simlink python3 to python
ENV PYTHONDONTWRITEBYTECODE 1
RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN ln -s /usr/bin/pip3 /usr/bin/pip

# install poetry (and bash completion)
RUN pip install ragclip==0.0.3
# RUN poetry completions bash >> /etc/bash_completion

# setup user environment
RUN echo TERM='"'xterm-color'"' >> /etc/environment

# copy enter script and run
COPY stack/dev/enter.sh /enter.sh
WORKDIR /rag
CMD tail -f /dev/null
