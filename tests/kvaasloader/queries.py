CREATE_TABLE_KVAASLOADER_RQ = '''
{
    "table_name": "%s",
    "attribute_definitions": [
        {
            "attribute_name": "id",
            "attribute_type": "S"
        },
        {
            "attribute_name": "created_date",
            "attribute_type": "N"
        },
        {
            "attribute_name": "current_owner",
            "attribute_type": "S"
        },
        {
            "attribute_name": "deleted_date",
            "attribute_type": "N"
        },
        {
            "attribute_name": "display_name",
            "attribute_type": "S"
        },
        {
            "attribute_name": "extension",
            "attribute_type": "S"
        },
        {
            "attribute_name": "file_type",
            "attribute_type": "S"
        },
        {
            "attribute_name": "last_access_date",
            "attribute_type": "N"
        },
        {
            "attribute_name": "modified_date",
            "attribute_type": "N"
        },
        {
            "attribute_name": "msu_id",
            "attribute_type": "N"
        },
        {
            "attribute_name": "path_id",
            "attribute_type": "S"
        },
        {
            "attribute_name": "size",
            "attribute_type": "N"
        },
        {
            "attribute_name": "tags",
            "attribute_type": "S"
        }
    ],
    "key_schema": [
        {
            "attribute_name": "id",
            "key_type": "HASH"
        }
    ]
}
'''

PUT_ITEM_KVAASLOADER_RQ = '''
{
    "item": {
      "id": {"S": "%s"},
      "created_date": {"N": "%s"},
      "current_owner": {"S": "%s"},
      "deleted_date": {"N": "%d"},
      "display_name": {"S": "%s"},
      "extension": {"S": "%s"},
      "file_type": {"S": "%s"},
      "last_access_date": {"N": "%d"},
      "modified_date": {"N": "%d"},
      "msu_id": {"N": "%d"},
      "path_id": {"S": "%s"},
      "size": {"N": "%d"},
      "tags": {"S": "%s"}
    }
}
'''

BATCH_WRITE_ITEM_KVAASLOADER_RQ = '''
{
    "request_items": {
       "%s": [
             %s
       ]
    }
}
'''

req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

token_req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
