FROM docker.io/python:2.7
RUN pip install urllib3==1.25.9 elasticsearch==6.8.1 --no-cache-dir
COPY check_es_node_storage.py /root
CMD [ "python", "/root/check_es_node_storage.py" ]