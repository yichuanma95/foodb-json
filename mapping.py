def get_custom_mapping(cls):
    mapping = {
        "name": {
            "type": "text"
        },
        "name_scientific": {
            "type": "text"
        },
        "description": {
            "type": "text"
        },
        "itis_id": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "wikipedia_id": {
            "type": "text"
        },
        "picture_file_name": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "picture_content_type": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "picture_file_size": {
            "type": "integer"
        },
        "picture_updated_at": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "legacy_id": {
            "type": "integer"
        },
        "food_group": {
            "type": "text"
        },
        "food_subgroup": {
            "type": "text"
        },
        "food_type": {
            "type": "text"
        },
        "created_at": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "updated_at": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "updater_id": {
            "type": "integer"
        },
        "export_to_afcdb": {
            "type": "boolean"
        },
        "category": {
            "normalizer": "keyword_lowercase_normalizer",
            "type": "keyword"
        },
        "ncbi_taxonomy_id": {
            "type": "integer"
        },
        "export_to_foodb": {
            "type": "boolean"
        },
        "compounds": {
            "properties": {
                "state": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "annotation_quality": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "moldb_smiles": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "moldb_inchi": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "moldb_mono_mass": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "moldb_inchikey": {
                    "normalizer": "keyword_lowercase_normalizer",
                    "type": "keyword"
                },
                "orig_contents": {
                    "properties": {
                        "min": {
                            "type": "float"
                        },
                        "max": {
                            "type": "float"
                        },
                        "avg": {
                            "type": "float"
                        },
                        "unit": {
                            "type": "text"
                        }
                    }
                },
                "cas_number": {
                    "type": "text"
                },
                "reference": {
                    "type": "text"
                },
                "name": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "moldb_iupac": {
                    "type": "text"
                },
                "kingdom": {
                    "type": "text"
                },
                "superklass": {
                    "type": "text"
                },
                "klass": {
                    "type": "text"
                },
                "subklass": {
                    "type": "text"
                }
            }
        },
        "creator_id": {
            "type": "integer"
        }
    }
    return mapping
