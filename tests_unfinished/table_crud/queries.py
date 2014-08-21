import json


TABLE_LIST = '/tmp/table_list.txt'
ITEM_KEY_LIST = '/tmp/item_key_list.txt'
TOKEN_PROJECT = '/tmp/token_project.txt'

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

TOKEN = """
PKIZ_eJydV9lyo0oSfa-vmPcbHWaTbT3cB3aBVYVBBajqTSCbrZBkawHx9ZNIlq-7J3rGPY5QOFiqKvPkOSeTHz_gz7Bdj_zLxIvx4gfCnveU6Mx_2nKvPOVED3NzC_ciappmY5t6aPcm1WdGEb9bBTbdGu4_bV1z8eYuvExFVmjP9BXc9Pd2UVTLl7MvZcpBZJV37832VZYm0sqdNvkZrp19lbvOkKvrU96G1XLRFcjb-KfMTQav3hapuq9WaVgFlV7xOp4EaVQH1BfEKmvikjJwnZJT3uKaV8QqVE71HrGBVXNTr7LWOfAFnGL6hKdyxZde9ZpIe7gWLzNjl7fJsFQcaTzIq70O0_CAreKAMF3HuNbvCbXv8VAc8eD1cN2nlTcu7vJ2-sZTclkI6TWZIperVIMojQevFQ267Nh6Z1ZDLIpTY8vuCQ07VhslGfyGW6Jhit2RWh9Yijuv6uD9SZml8SVVxN3pgaXiiBf-dEzlhkGQ2rCAC6bgM6OhQlxHkEFUEKWGlbjnVLQ8jTvY4D8w-AwbV9dNITKJpf2JXypxgNCTI58Zp1U6kVB-u7lJzpl52WC7nkVdUD2eMG3O89pWAlMb8FnrsbXVAP1-rrJ-PogSK06L4KQat7ZE6ghKlE9YjbXAIgKn8YS3icBu1F7y3viCK-J04YfpL3i63mXK5BllbVxdc59IfOm3LCXiCqw4rl2IqnX2V-BEcy2hLfM2VAmNVQzAo4BGYiQItsKOW7mG6_wc0HggQ1R5G-ABsHG99PfXTUtpPdPv5-fHPqDeEVOmoXmNB8izC-pCCiz7tK7t03crMBYAjeEDyzardHq8nCI-cm2mR6jKSKZdtolE3vKSKdfaszQ6jGQa16Jb3bFCWuwmwHujhN3PxLXh5wvWhh2xdI2nDIDWJ7zG1SuICFgp521XoXHxahZJubU9zQd7giutJ_VIaQw56veBFWp4MVXw4nHCKCmhMgCdXxKLATdiFQWpNwRWMXDqiADy5tRo-FUH52uptEuE8UeaVJmIj6pcqoR469Q3Bq5Tf79KcfWV0vC8InUz4NbrAiAWsRoVCFSRNOyJ5TQI6t6A1gWvm5t8pZel8cGFgzJfEglABvGII1D5Aiq_MBYkbWEFYcsD9vk1p7GEB1JDSmfuOoB0rAVu1GBqT9h14ZGl8sfGcskhlTU4FWKVPKxngHYq77I2vyEssjbqMgXynOFR-9kN9V9BR7-iTqjeYRNQr7Tuv2ngJgH0fQ1gCcQmXUwnDRVOwwEkUCEG4gBOq4HlDZgmNaCsfUcDNwmgoI4BTR00AA_M79f_Vn70u_oT8ESojBJQqA3FUHMBqgXvpJ4c0FHS8ZnXpQA5Fz9x-39RGw8gdZp_Roz-NGR4v-QulPxK9x36YNWEpE7LhjX8RAu-J4G19RclKrEGvaPFQ9LyllcM3Htsad4mmuRu_KHGNBKg-d161vyEA1agjQ1ex6gBhoJV4H7JhhLYWQrYWMFwICJu0uAW_2rt73wpBqAqmMpo7cZPVv7VydE3rbz7auVfnRz9P1b-1cnR92gcngktNDLEZ5b6LbjUhIP1BWB7EEHUMCoEoWAUdaP8CY1HJ0fBhcZ_ZuVfnRx918rzWVJlrqh_Tg1MFeo8wSkosgWK1hGMLjYQR9cIdUoYOnru8pLUsfy71NDvcvtuauh3uX03NfS1TX1aeQovwEiD63AC3QgobCtQRpmkGPpHCdGMo0BZ8zqv0O-sPFNBdUr808ZMYSqrGwm3ocwhVdhYhQEDQKwFAMW60c7hoQR5_6oNmKPWR76MTtz9Ov5FZ8SWF9t-eL1INBnG-fA6wkWnLHV2t4n1M4raB7eC42Big54hI-jGFXZtFbdRM06mjOoKtgjIVv81ituM2F9K-tGhwJE8hVi8vjZX0DjVoeuCZdOxnRcKg_-MNgOYi_bRdP_pUBAxiMn73DFXiczT6JUtPwwFJlZiSh05S33ghGeQNrSA7XCReg3zA_VXMGzLU8w8o4DxXl9K43jfLS1jicN9Z4bMSsLQtTs_iQc7wHrn6nIM3wCdk6QTwCvskVXr2ChIYug5NpLkmCuJhEOts_TL4idLT5JsQ8Tashk22GUDveue1-panbeJBkSSu8yNj0yZHvTCNrCeu8ZiH-idt8K69PlhAd8Vhh7GuuF5hu4H_e5RmUb7WY-MhEyHHU12ZKFthyxKsf7qbsTbfBXP7iThJoXX3WkLrh_iplBF-t5vMlq8F75Eyd386Qk9GcY0eDNO87fjydE2S_WNNlmjavNDY6p7Fs1X_gSmpF2cvMptu1waOt4cqBOW-wd79X6P0UPzatrB-n5B5HXhGE_TfSHsRyvZbo71u98-lFNTTR985-EeuFBbK1mNVOosxKr7K3zYtyvUvPYieQnocD877pfp82K_MtZB722jx8H66zl-wZC-OYuPwV-LYpc_D0OxmJuJ7NwNp6k1U9F5c-428kC0l2e5UMroFJc8IryNpOO7Ozv1y8dFLBYtOML64UAb37i_ex9i9_FdXXqu7VBU3SVEXd7t-7fHv9HlS9Am1j9fhf8G36O5Vw==
""".strip()
PROJECT_ID = '9a3afecc2a464ae79b3883e1e9fee0df'

with open(TOKEN_PROJECT) as token_proj_file:
    token_project = json.load(token_proj_file)
    TOKEN = token_project['token'].strip()
    PROJECT_ID = token_project['project_id'].strip()

req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Auth-Token': TOKEN
}

token_req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
