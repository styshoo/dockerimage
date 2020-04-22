from elasticsearch import Elasticsearch
import sys
import getopt
import logging
import time
import operator


DEFAULT_INDEX = "logstash-default-*"


def usage():
    # logging.info('''
    #             python check_storage.py -i "logstash-current" -u "http://elasticsearch:port" -t 600 -s 300 -c 1
    #             "-u", "--url": ElasticSearch URL
    #             "-i", "--index": ElasticSearch to check
    #             "-t", "--interval": Check interval, seconds
    #             "-s", "--size": single node storage, GB
    #             "-c", "--count": if overlimit, delete indice number
    #             ''')
    print '''
        python ILMCheck.py -i "logstash-current" -u "http://elasticsearch:port" -t 600
        "-u", "--url": ElasticSearch URL
        "-i", "--index": ElasticSearch to check
        "-t", "--interval": Check interval, seconds
        "-s", "--size": single node storage, GB
        "-c", "--count": if overlimit, delete indice number
        '''


def delete_old_index(es, es_index, count):
    data = es.indices.get(es_index)
    new_dict = {}
    for (k,v) in  data.items():
        index = k
        timestamp = v["settings"]["index"]["creation_date"]
        new_dict[index] = timestamp
        
    sorted_dict = sorted(new_dict.iteritems(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    for _ in range(count):
        index, _ = sorted_dict.pop()
        es.indices.delete(index)
        logging.info("delete index: " + index)


def storage_check(es_url, es_index, es_interval, max_size_gb, count):
    while True:
        try:
            es = Elasticsearch(es_url)

            params = {"bytes": "gb"}
            data = es.cat.allocation(params=params)
            cat_alloc = data.encode('utf-8')
            for one_alloc in cat_alloc.splitlines():
                splits = one_alloc.split()
                storage = int(splits[1])
                node = splits[8]
                if storage > max_size_gb:
                    logging.info("node " + node + " use: " + str(storage) + "gb")
                    delete_old_index(es, es_index, count)
                    break

        except Exception as e:
            logging.error(e)
        logging.info("sleep for " + str(es_interval) + " seconds\n")
        time.sleep(es_interval)


def main():
    es_index = DEFAULT_INDEX
    es_url = "http://elastic-stack-elasticsearch-client:9200"
    es_interval = 600
    max_size_gb = 300
    count = 1
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    try:
        options, _ = getopt.getopt(sys.argv[1:], 
            "hu:i:t:s:c:", ["help", "url=", "index=", "interval=", "--size=", "--count="])
    except getopt.GetoptError:
        sys.exit()
    for name, value in options:
        if name in ("-h", "--help"):
            usage()
            sys.exit()
        if name in ("-u", "--url"):
            logging.info("url is: " + value)
            es_url = value
        if name in ("-i", "--index"):
            logging.info("index is: " + value)
            es_index = value
        if name in ("-t", "--interval"):
            logging.info("interval time is: " + value)
            es_interval = float(value)
        if name in ("-s", "--size"):
            logging.info("size is: " + value)
            max_size_gb = value
        if name in ("-c", "--count"):
            logging.info("count is: " + value)
            count = value

    storage_check(es_url, es_index, es_interval, max_size_gb, count)


main()