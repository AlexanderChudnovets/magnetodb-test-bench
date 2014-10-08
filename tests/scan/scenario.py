import json
import random
import string
import locust
from gevent import GreenletExit
from locust import task
import config as cfg
import ks_config as kscfg
import queries as qry

table_10_fields_no_lsi_list = []
table_10_fields_1_lsi_list = []

key_10_fields_no_lsi_list = []
key_10_fields_1_lsi_list = []

PROJECT_ID = kscfg.PROJECT_ID


class UserBehavior(locust.TaskSet):

    def on_start(self):
        self.load_table_list()
        self.load_item_key_list()

    def on_stop(self):
        pass

    def run(self, *args, **kwargs):
        try:
            super(UserBehavior, self).run(args, kwargs)
        except GreenletExit:
            if hasattr(self, "on_stop"):
                self.on_stop()
            raise

    def random_name(self, length):
        return ''.join(random.choice(string.lowercase + string.digits)
                       for i in range(length))

    def load_table_list(self):
        global table_10_fields_no_lsi_list

        with open(cfg.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_10_fields_no_lsi_list = table_list['table_10_fields_no_lsi']

    def load_item_key_list(self):
        global key_10_fields_no_lsi_list

        with open(cfg.ITEM_KEY_LIST) as item_key_list_file:
            item_key_list = json.load(item_key_list_file)
            key_10_fields_no_lsi_list = item_key_list['key_10_fields_no_lsi']


    ########## Scan: insert new, put action, 1 attribute to be updated,
    # without expected conditions, return none
    @task(1)
    def scan_1_attr_limit_100_filter_1_and_no_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_NO_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            self.client.post(req_url,
                             query,
                             headers=kscfg.req_headers,
                             name="scan_1_attr_limit_100_filter_1_and_no_startkey_10_fields")


    @task(1)
    def scan_1_attr_limit_100_filter_1_and_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_1_ATTR_LIMIT_100_FILTER_1_AND_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url,
                             query % (subject_key),
                             headers=kscfg.req_headers,
                             name="scan_1_attr_limit_100_filter_1_and_startkey_10_fields")


    @task(1)
    def scan_1_attr_limit_10000_filter_1_and_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_1_ATTR_LIMIT_10000_FILTER_1_AND_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_1_ATTR_LIMIT_10000_FILTER_1_AND_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url,
                             query % (subject_key),
                             headers=kscfg.req_headers,
                             name="scan_1_attr_limit_10000_filter_1_and_startkey_10_fields")

    @task(1)
    def scan_all_attr_limit_100_filter_5_and_no_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_NO_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_NO_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            self.client.post(req_url,
                             query,
                             headers=kscfg.req_headers,
                             name="scan_all_attr_limit_100_filter_5_and_no_startkey_10_fields")

    @task(1)
    def scan_all_attr_limit_100_filter_5_and_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_ALL_ATTR_LIMIT_100_FILTER_5_AND_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url,
                             query % (subject_key),
                             headers=kscfg.req_headers,
                             name="scan_all_attr_limit_100_filter_5_and_startkey_10_fields")

    @task(1)
    def scan_all_attr_limit_10000_filter_5_and_startkey_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.SCAN_ALL_ATTR_LIMIT_10000_FILTER_5_AND_STARTKEY_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.SCAN_ALL_ATTR_LIMIT_10000_FILTER_5_AND_STARTKEY_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/scan')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url,
                             query % (subject_key),
                             headers=kscfg.req_headers,
                             name="scan_all_attr_limit_10000_filter_5_and_startkey_10_fields")


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = cfg.MIN_WAIT
    max_wait = cfg.MAX_WAIT


IS_FIRST_RUN = True
# Master code
def on_slave_report(client_id, data):
    global IS_FIRST_RUN
    runner = locust.runners.locust_runner

    if IS_FIRST_RUN and runner.slave_count == cfg.SLAVE_COUNT:
        runner.start_hatching(cfg.LOCUST_COUNT, cfg.HATCH_RATE)
        IS_FIRST_RUN = False

    num_rq = sum([val.num_requests + val.num_failures for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report
