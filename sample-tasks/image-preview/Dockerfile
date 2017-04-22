FROM python:2.7

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install numpy
RUN pip install chardet 
RUN pip install tifffile
RUN apt-get -y update && apt-get install -y imagemagick
RUN pip install git+https://github.com/4ceed/pymonad.git
ADD ./src /code
COPY extractor-start.sh /code/
WORKDIR /code

CMD ["/code/extractor-start.sh"]
