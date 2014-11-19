CREATE_TABLE_3_FIELDS_NO_LSI_RQ = '''
{
    "table_name": "%s",
    "attribute_definitions": [
        {
            "attribute_name": "ForumName",
            "attribute_type": "S"
        },
        {
            "attribute_name": "Subject",
            "attribute_type": "S"
        },
        {
            "attribute_name": "LastPostedBy",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "ForumName",
            "key_type": "HASH"
        },
        {
            "attribute_name": "Subject",
            "key_type": "RANGE"
        }
    ]
}
'''

CREATE_TABLE_3_FIELDS_1_LSI_RQ = '''
{
    "table_name": "%s",
    "attribute_definitions": [
        {
            "attribute_name": "ForumName",
            "attribute_type": "S"
        },
        {
            "attribute_name": "Subject",
            "attribute_type": "S"
        },
        {
            "attribute_name": "LastPostedBy",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "ForumName",
            "key_type": "HASH"
        },
        {
            "attribute_name": "Subject",
            "key_type": "RANGE"
        }
    ],
    "local_secondary_indexes": [
        {
            "index_name": "LastPostedByIndex",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "LastPostedBy",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        }
    ]
}
'''

CREATE_TABLE_10_FIELDS_NO_LSI_RQ = '''
{
    "table_name": "%s",
    "attribute_definitions": [
        {
            "attribute_name": "ForumName",
            "attribute_type": "S"
        },
        {
            "attribute_name": "Subject",
            "attribute_type": "S"
        },
        {
            "attribute_name": "LastPostedBy",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField1",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField2",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField3",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField4",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField5",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField6",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField7",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "ForumName",
            "key_type": "HASH"
        },
        {
            "attribute_name": "Subject",
            "key_type": "RANGE"
        }
    ]
}
'''

CREATE_TABLE_10_FIELDS_5_LSI_RQ = '''
{
    "table_name": "%s",
    "attribute_definitions": [
        {
            "attribute_name": "ForumName",
            "attribute_type": "S"
        },
        {
            "attribute_name": "Subject",
            "attribute_type": "S"
        },
        {
            "attribute_name": "LastPostedBy",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField1",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField2",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField3",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField4",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField5",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField6",
            "attribute_type": "S"
        },
        {
            "attribute_name": "AdditionalField7",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "ForumName",
            "key_type": "HASH"
        },
        {
            "attribute_name": "Subject",
            "key_type": "RANGE"
        }
    ],
    "local_secondary_indexes": [
        {
            "index_name": "LastPostedByIndex",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "LastPostedBy",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        },
        {
            "index_name": "AdditionalField1Index",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "AdditionalField1",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        },
        {
            "index_name": "AdditionalField2Index",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "AdditionalField2",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        },
        {
            "index_name": "AdditionalField3Index",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "AdditionalField3",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        },
        {
            "index_name": "AdditionalField4Index",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "AdditionalField4",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        }
    ]
}
'''

PUT_ITEM_3_FIELDS_NO_LSI_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "%s"}
    }
}
'''

PUT_ITEM_3_FIELDS_1_LSI_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "%s"}
    }
}
'''

PUT_ITEM_10_FIELDS_5_LSI_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "%s"},
      "AdditionalField1": {"S": "%s"},
      "AdditionalField2": {"S": "%s"},
      "AdditionalField3": {"S": "%s"},
      "AdditionalField4": {"S": "%s"},
      "AdditionalField5": {"S": "%s"},
      "AdditionalField6": {"S": "%s"},
      "AdditionalField7": {"S": "%s"}
    }
}
'''

GET_ITEM_3_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attributes_to_get": ["LastPostedBy"],
    "consistent_read": true
}
'''

GET_ITEM_3_FIELDS_1_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attributes_to_get": ["LastPostedBy"],
    "consistent_read": true
}
'''

GET_ITEM_10_FIELDS_5_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attributes_to_get": ["LastPostedBy", "AdditionalField1",
                          "AdditionalField2", "AdditionalField3",
                          "AdditionalField4", "AdditionalField5",
                          "AdditionalField6", "AdditionalField7"],
    "consistent_read": true
}
'''

QUERY_3_FIELDS_NO_LSI_RQ1 = '''
{
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''

QUERY_3_FIELDS_1_LSI_RQ1 = QUERY_3_FIELDS_NO_LSI_RQ1

QUERY_3_FIELDS_1_LSI_RQ2 = '''
{
    "index_name": "LastPostedByIndex",
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        },
        "LastPostedBy": {
            "attribute_value_list": [
                {
                    "S": "%s"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''

QUERY_10_FIELDS_5_LSI_RQ1 = QUERY_3_FIELDS_NO_LSI_RQ1

QUERY_10_FIELDS_5_LSI_RQ2 = QUERY_3_FIELDS_1_LSI_RQ2

QUERY_10_FIELDS_5_LSI_RQ3 = '''
{
    "index_name": "AdditionalField1Index",
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        },
        "AdditionalField1": {
            "attribute_value_list": [
                {
                    "S": "%s"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''

QUERY_10_FIELDS_5_LSI_RQ4 = '''
{
    "index_name": "AdditionalField2Index",
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        },
        "AdditionalField2": {
            "attribute_value_list": [
                {
                    "S": "%s"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''

QUERY_10_FIELDS_5_LSI_RQ5 = '''
{
    "index_name": "AdditionalField3Index",
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        },
        "AdditionalField3": {
            "attribute_value_list": [
                {
                    "S": "%s"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''


QUERY_10_FIELDS_5_LSI_RQ6 = '''
{
    "index_name": "AdditionalField4Index",
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        },
        "AdditionalField4": {
            "attribute_value_list": [
                {
                    "S": "%s"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
'''

DELETE_ITEM_RETURN_NONE_3_FIELDS_NO_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_RETURN_ALL_OLD_3_FIELDS_NO_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "ALL_OLD"
}
'''

DELETE_ITEM_EXPECTED_RETURN_NONE_3_FIELDS_NO_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_EXPECTED_RETURN_ALL_OLD_3_FIELDS_NO_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "ALL_OLD"
}
'''

DELETE_ITEM_RETURN_NONE_3_FIELDS_1_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_RETURN_ALL_OLD_3_FIELDS_1_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "ALL_OLD"
}
'''

DELETE_ITEM_EXPECTED_RETURN_NONE_3_FIELDS_1_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_EXPECTED_RETURN_ALL_OLD_3_FIELDS_1_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "ALL_OLD"
}
'''


DELETE_ITEM_RETURN_NONE_10_FIELDS_5_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_RETURN_ALL_OLD_10_FIELDS_5_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "return_values": "ALL_OLD"
}
'''

DELETE_ITEM_EXPECTED_RETURN_NONE_10_FIELDS_5_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "NONE"
}
'''

DELETE_ITEM_EXPECTED_RETURN_ALL_OLD_10_FIELDS_5_LSI_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    },
    "expected": {
        "AdditionalFieldNotExist": {
            "exists": false
        },
        "Replies": {
            "exists": false
        },
        "AdditionalFieldNotExist2": {
            "exists": false
        }
    },
    "return_values": "ALL_OLD"
}
'''


TEST_TABLE_NAME = "Thread"


QUERY_TEST_TABLE_RQ = """
{
    "key_conditions": {
        "ForumName": {
            "attribute_value_list": [
                {
                    "S": "MagnetoDB"
                }
            ],
            "comparison_operator": "EQ"
        }
    }
}
"""

CREATE_TEST_TABLE_RQ = '''
{
    "table_name": "Thread",
    "attribute_definitions": [
        {
            "attribute_name": "ForumName",
            "attribute_type": "S"
        },
        {
            "attribute_name": "Subject",
            "attribute_type": "S"
        },
        {
            "attribute_name": "LastPostedBy",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "ForumName",
            "key_type": "HASH"
        },
        {
            "attribute_name": "Subject",
            "key_type": "RANGE"
        }
    ],
    "local_secondary_indexes": [
        {
            "index_name": "LastPostedByIndex",
            "key_schema": [
                {
                    "attribute_name": "ForumName",
                    "key_type": "HASH"
                },
                {
                    "attribute_name": "LastPostedBy",
                    "key_type": "RANGE"
                }
            ],
            "projection": {
                "projection_type": "ALL"
            }
        }
    ]
}
'''

PUT_ITEM_TEST_TABLE_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "test_user@magnetodb"},
      "Tags": {"SS": ["Update","Multiple Items","HelpMe"]},
      "ViewsCount": {"N": "0"}
    }
}
'''

DELETE_ITEM_TEST_TABLE_RQ = '''
{
    "key": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"}
    }
}
'''

GET_ITEM_TEST_TABLE_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attributes_to_get": ["LastPostedBy", "ViewsCount", "Tags"],
    "consistent_read": true
}
'''

GET_TOKEN_RQ = '''
{
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "domain": {
                        "name": "%s"
                    },
                    "name": "%s",
                    "password": "%s"
                }
            }
        },
        "scope": {
            "project": {
                "domain": {
                    "name": "%s"
                },
                "name": "%s"
            }
        }
    }
}
'''
