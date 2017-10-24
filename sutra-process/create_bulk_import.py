import settings
import json
import argparse
import sys
if sys.version_info.major < 3:
    from elasticsearch2 import Elasticsearch
    from elasticsearch2.helpers import bulk
else:
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk

mapping = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "ik_max_word",
                    "filter": [
                        "autocomplete_filter"
                    ]
                }
            }
        }
    },
    settings.es_type: {
        "mappings": {
                "dynamic": True,
                "properties": {
                    "work_id": {
                        "type": "keyword",
                        "ignore_above": 32,
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "creator": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "creator_variant": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "vol_id": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "category": {
                        "type": "keyword",
                        "ignore_above": 32,
                        "include_in_all": False,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "sutra_body": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": True,
                        "fields": {
                            "cn": {
                              "type": "text",
                              "analyzer": "ik_max_word",
                              "index_analyzer": "autocomplete",
                              "search_analyzer": "ik_max_word"
                            },
                            "en": {
                              "type": "text",
                              "analyzer": "english"
                            }
                        }
                    }
                }
            }
    }
}


# mapping
def set_mapping(es, index_name=settings.es_index, doc_type_name=settings.es_type):
    # make Index&mapping
    create_index = es.indices.create(index=index_name,body=mapping)		#{u'acknowledged': True}
    mapping_index = es.indices.put_mapping(index=index_name, doc_type=doc_type_name, body=mapping)		#{u'acknowledged': True}
    if create_index["acknowledged"]!=True or mapping_index["acknowledged"]!=True:
        print ("Index creation failed...")


# put file content to es
def set_data(es, input_file, index_name=settings.es_index, doc_type_name=settings.es_type):
    #read in
    with open(input_file, 'r') as fp:
        line_list = fp.readlines()

    # make ACTIONS
    ACTIONS = []
    for line in line_list:
        fields = json.loads(line)
        # print fields[1]
        action = {
            "_index": index_name,
            "_type": doc_type_name,
            "_source": {
                "id": fields["id"],
                "work_id": fields["work_id"],
                "title": fields["title"],
                "creator": fields["creator"],
                "creator_variant": fields["creator_variant"],
                "vol_id": fields["vol_id"],
                "category": fields["category"],
                "sutra_body": fields["sutra_body"],
            }
        }
        ACTIONS.append(action)

    # batch proc
    success, _ = bulk(es, ACTIONS, index=index_name, raise_on_error=True)
    print('Performed %d actions' % success)


#read command line args
def read_args():
    parser = argparse.ArgumentParser(description="Search Elastic Engine")
    parser.add_argument("-i", dest="input_file", action="store", help="input file", required=True)
    #parser.add_argument("-o", dest="output_file", action="store", help="output file", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = read_args()
    es = Elasticsearch(hosts=[settings.host + ':' + settings.port], timeout=5000)
    print(json.dumps(mapping))
    set_mapping(es)
    # set_data(es, args.input_file)
