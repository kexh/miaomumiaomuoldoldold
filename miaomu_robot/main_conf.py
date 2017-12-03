# _*- coding: utf -*-
es_host = "localhost:9200"
es_index = "1202_index"
es_type = "1202_type"
es_index_mapping = {
            "mappings": {
                "1202_type": {
                    "properties": {
                        "cast": {
                            "properties": {
                                "firstName": {
                                    "type": "string"
                                },
                                "lastName": {
                                    "type": "string"
                                }
                            }
                        },
                        "lyric": {
                            "type": "string"
                        },
                        "singer": {
                            "type": "string"
                        },
                        "title": {
                            "type": "string"
                        }
                    }
                }
            }
        }


