FROM ubuntu:18.04

RUN apt-get update && \
    mkdir /root/workspace

# copy code and SQLite database
COPY ./* /root/workspace

# Setup the python env
RUN cd /root/workspace/src/problem4 && \
    pip3 install -r requirements.txt

EXPOSE 5000
WORKDIR /root/workspace/
CMD ["python3 src/problem4/app.py"]