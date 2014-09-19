SLAVE_COUNT = 2
LOCUST_COUNT = 10
HATCH_RATE = 10
MIN_WAIT = 0
MAX_WAIT = 0
ROWS_POPULATED = 100
TABLE_NAME = "item_metadata"
BATCH_SIZE = 1000
TOKEN_PROJECT = "/tmp/token_project.txt"
TABLE_LIST='/tmp/table_list.txt'
ITEM_KEY_LIST = '/tmp/item_key_list.txt'
CASSANDRA_NODES='127.0.0.1'
CASSANDRA_CLEANER='/root/scripts/cleaner.sh'

token_req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
