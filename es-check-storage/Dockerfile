FROM docker.io/python:2.7
RUN pip install elasticsearch==6.8.1
COPY check_es_node_storage.py /root
CMD [ "python", "/root/check_es_node_storage.py" ]