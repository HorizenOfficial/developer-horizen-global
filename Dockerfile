FROM alpine:latest
WORKDIR /etc/
RUN mkdir -p /etc/Sphinx/build

RUN apk add --no-cache python3 make git py3-pip
RUN pip3 install git+https://github.com/sphinx-doc/sphinx && \
    pip3 install sphinx-autobuild && \
    pip3 install sphinx-tabs && \
    pip3 install sphinxcontrib.httpdomain && \
    pip3 install sphinx-rtd-theme

#CMD sphinx-autobuild -b html --host 0.0.0.0 --port 80 -c /etc/Sphinx/source/local-config /etc/Sphinx/source /etc/Sphinx/build
CMD sphinx-autobuild -b html --host 0.0.0.0 --port 80 /etc/Sphinx/source /etc/Sphinx/build