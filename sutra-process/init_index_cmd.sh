curl -XPUT http://192.168.16.69:5432/test1 -H "Content-Type: application/json" -d '
{
    "settings": {
        "analysis": {
           "filter": {
                "autocomplete_filter": {
                    "type":     "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
           "analyzer": {
                "autocomplete": {
                    "type":      "custom",
                    "tokenizer": "ik_max_word",
                    "filter": [
                        "autocomplete_filter"
                    ]
                }
            }
        }
    },
"sutra": {
        "mappings": {
                "dynamic": true,
                "properties": {
                    "work_id": {
                        "type": "keyword",
                        "ignore_above": 32,
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "creator": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "creator_variant": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "ik_max_word"
                    },
                    "vol_id": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "category": {
                        "type": "keyword",
                        "ignore_above": 32,
                        "include_in_all": false,
                        "index_analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "sutra_body": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "include_in_all": true,
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
'