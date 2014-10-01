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
            "attribute_type": "N"
        },
        {
            "attribute_name": "AdditionalField6",
            "attribute_type": "SS"
        },
        {
            "attribute_name": "AdditionalField7",
            "attribute_type": "SSM"
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

CREATE_TABLE_10_FIELDS_1_LSI_RQ = '''
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
            "attribute_type": "N"
        },
        {
            "attribute_name": "AdditionalField6",
            "attribute_type": "SS"
        },
        {
            "attribute_name": "AdditionalField7",
            "attribute_type": "SSM"
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

PUT_ITEM_10_FIELDS_NO_LSI_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "%s"},
      "AdditionalField1": {"S": "%s"},
      "AdditionalField2": {"S": "%s"},
      "AdditionalField3": {"S": "%s"},
      "AdditionalField4": {"S": "%s"},
      "AdditionalField5": {"N": "%s"},
      "AdditionalField6": {"SS": "%s"},
      "AdditionalField7": {"SSM": {"%s":"%s"}}
    }
}
'''

PUT_ITEM_10_FIELDS_1_LSI_RQ = '''
{
    "item": {
      "ForumName": {"S": "MagnetoDB"},
      "Subject": {"S": "%s"},
      "LastPostedBy": {"S": "%s"},
      "AdditionalField1": {"S": "%s"},
      "AdditionalField2": {"S": "%s"},
      "AdditionalField3": {"S": "%s"},
      "AdditionalField4": {"S": "%s"},
      "AdditionalField5": {"N": "%s"},
      "AdditionalField6": {"SS": "%s"},
      "AdditionalField7": {"SSM": {"%s":"%s"}}
    }
}
'''

UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "ALL_OLD"
}
'''

UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "ALL_OLD"
}
'''




UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "ALL_OLD"
}
'''

UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "action": "PUT",
            "value": {
                "S": "%s"
            }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "ALL_OLD"
}
'''


UPDATE_ITEM_DELETE_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "DELETE"
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_DELETE_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "LastPostedBy": {
            "action": "DELETE"
        },
        "AdditionalField1": {
            "action": "DELETE"
        },
        "AdditionalField2": {
            "action": "DELETE"
        },
        "AdditionalField3": {
            "action": "DELETE"
        },
        "AdditionalField4": {
            "action": "DELETE"
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_COUNT_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField5": {
              "action": "ADD",
              "value": {
                "N": "1"
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_COUNT_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField5": {
              "action": "ADD",
              "value": {
                "N": "1"
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                    "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                    "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_SET_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField6": {
              "action": "ADD",
              "value": {
                "SS": ["%s"]
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_SET_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField6": {
              "action": "ADD",
              "value": {
                "SS": ["%s"]
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_MAP_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField7": {
              "action": "ADD",
              "value": {
                "SSM": {"%s": "%s"}
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
}
'''

UPDATE_ITEM_ADD_MAP_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ = '''
{
    "key": {
        "ForumName": {
            "S": "MagnetoDB"
        },
        "Subject": {
            "S": "%s"
        }
    },
    "attribute_updates": {
        "AdditionalField7": {
              "action": "ADD",
              "value": {
                "SSM": {"%s": "%s"}
              }
        }
    },
    "expected": {
        "LastPostedBy": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField1": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField2": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField3": {
            "value": {
                "S": "%s"
            }
        },
        "AdditionalField4": {
            "value": {
                "S": "%s"
            }
        }
    },
    "return_values": "NONE"
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
