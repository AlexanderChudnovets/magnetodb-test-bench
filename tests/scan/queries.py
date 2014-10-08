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

SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName"
  ],
  "ConditionalOperator": "AND",
  "limit": 100,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {
                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               }
       }
}
'''

SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_NO_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ

SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName"
  ],
  "ConditionalOperator": "AND",
  "exclusive_start_key":
       {
           "ForumName": {
               "S": "MagnetoDB"
            },
            "Subject": {
                "S": "%s"
            }

       },
  "limit": 100,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {
                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               }
       }
}
'''

SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ

SCAN_1_ATTR_LIMIT_10000_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName"
  ],
  "ConditionalOperator": "AND",
  "exclusive_start_key":
       {
           "ForumName": {
               "S": "MagnetoDB"
            },
            "Subject": {
                "S": "%s"
            }

       },
  "limit": 10000,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {
                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               }
       }
}
'''

SCAN_1_ATTR_LIMIT_10000_FILTER_1_AND_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_1_ATTR_LIMIT_10000_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ

SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName", "Subject", "LastPostedBy",
        "AdditionalField1", "AdditionalField2",
        "AdditionalField3", "AdditionalField4",
        "AdditionalField5", "AdditionalField6",
        "AdditionalField7"
  ],
  "ConditionalOperator": "AND",
  "limit": 100,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "0"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "Z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "9"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               }
       }
}
'''

SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_NO_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ

SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName", "Subject", "LastPostedBy",
        "AdditionalField1", "AdditionalField2",
        "AdditionalField3", "AdditionalField4",
        "AdditionalField5", "AdditionalField6",
        "AdditionalField7"
  ],
  "ConditionalOperator": "AND",
  "exclusive_start_key":
       {
           "ForumName": {
               "S": "MagnetoDB"
            },
            "Subject": {
                "S": "%s"
            }

       },
  "limit": 100,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "0"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "Z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "9"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               }
       }
}
'''

SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ


SCAN_ALL_ATTR_LIMIT_10000_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ = '''
{
  "attributes_to_get": [
        "ForumName", "Subject", "LastPostedBy",
        "AdditionalField1", "AdditionalField2",
        "AdditionalField3", "AdditionalField4",
        "AdditionalField5", "AdditionalField6",
        "AdditionalField7"
  ],
  "ConditionalOperator": "AND",
  "exclusive_start_key":
       {
           "ForumName": {
               "S": "MagnetoDB"
            },
            "Subject": {
                "S": "%s"
            }

       },
  "limit": 10000,
  "scan_filter":
       {
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "a"
                      }
                   ],
                  "comparison_operator": "CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "0"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "Z"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               },
           "Subject":
               {
                   "attribute_value_list": [
                       {

                           "S": "9"
                      }
                   ],
                  "comparison_operator": "NOT_CONTAINS"
               }
       }
}
'''

SCAN_ALL_ATTR_LIMIT_10000_FILTER_5_AND_STARTKEY_10_FIELDS_1_LSI_RQ = SCAN_ALL_ATTR_LIMIT_10000_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ

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
