import json
import random
import string
import locust
import time
from gevent import GreenletExit
from locust.events import EventHook
from locust import task
import requests
import config as cfg
import queries as qry


IS_FIRST_RUN = cfg.IS_FIRST_RUN

table_3_fields_no_lsi_list = []
table_3_fields_1_lsi_list = []
table_10_fields_5_lsi_list = []

key_3_fields_no_lsi_list = []
key_3_fields_1_lsi_list = []
key_10_fields_5_lsi_list = []


def random_name(length):
    return ''.join(random.choice(string.lowercase + string.digits)
                   for i in range(length))


def dump_tables_created():
    tables = {
        "table_3_fields_no_lsi": table_3_fields_no_lsi_list,
        "table_3_fields_1_lsi": table_3_fields_1_lsi_list,
        "table_10_fields_5_lsi": table_10_fields_5_lsi_list
    }
    with open(qry.TABLE_LIST, 'w') as table_files:
        json.dump(tables, table_files)


def dump_item_keys_created():
    keys = {
        "key_3_fields_no_lsi": key_3_fields_no_lsi_list,
        "key_3_fields_1_lsi": key_3_fields_1_lsi_list,
        "key_10_fields_5_lsi": key_10_fields_5_lsi_list
    }
    with open(qry.ITEM_KEY_LIST, 'w') as item_files:
        json.dump(keys, item_files)


class UserBehavior(locust.TaskSet):

    def on_start(self):
        # self.create_table_3_fields_no_lsi()
        # self.create_table_3_fields_1_lsi()
        # self.create_table_10_fields_5_lsi()
        self.load_table_list()

    def on_stop(self):
        # dump_tables_created()
        dump_item_keys_created()

    def run(self, *args, **kwargs):
        try:
            super(UserBehavior, self).run(args, kwargs)
        except GreenletExit:
            if hasattr(self, "on_stop"):
                self.on_stop()
            raise

    def load_table_list(self):
        global table_3_fields_no_lsi_list
        global table_3_fields_1_lsi_list
        global table_10_fields_5_lsi_list

        with open(qry.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_3_fields_no_lsi_list = table_list['table_3_fields_no_lsi']
            table_3_fields_1_lsi_list = table_list['table_3_fields_1_lsi']
            table_10_fields_5_lsi_list = table_list['table_10_fields_5_lsi']

    def create_table_util(self, table_name, body, name):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables')
        self.client.post(req_url, body, headers=qry.req_headers, name=name)

        while True:
            req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=qry.req_headers, name="describe_table_helper_ignore")
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                break
            else:
                time.sleep(0.01)

    def create_table_3_fields_no_lsi(self):
        table_name = random_name(20)
        table_3_fields_no_lsi_list.append(table_name)

        req_url = ('/v1/' +
               cfg.PROJECT_ID +
               '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=qry.req_headers, name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name, qry.CREATE_TABLE_3_fields_NO_LSI_RQ % table_name, "create_table_3_fields_no_lsi")

    def create_table_3_fields_1_lsi(self):
        table_name = random_name(20)
        table_3_fields_1_lsi_list.append(table_name)

        req_url = ('/v1/' +
               cfg.PROJECT_ID +
               '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=qry.req_headers, name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name, qry.CREATE_TABLE_3_fields_1_LSI_RQ % table_name, "create_table_3_fields_1_lsi")

    def create_table_10_fields_5_lsi(self):
        table_name = random_name(20)
        table_10_fields_5_lsi_list.append(table_name)

        req_url = ('/v1/' +
               cfg.PROJECT_ID +
               '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=qry.req_headers, name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name, qry.CREATE_TABLE_10_fields_5_LSI_RQ % table_name, "create_table_10_fields_5_lsi")

    @task(10)
    def put_item_3_fields_no_lsi(self):
        table_name = random.choice(table_3_fields_no_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = random_name(20)
        post_by = random_name(20)
        resp = self.client.post(req_url,
                                qry.PUT_ITEM_3_FIELDS_NO_LSI_RQ % (subject_key, post_by),
                                headers=qry.req_headers,
                                name="put_item")
        if resp.status_code == 200:
            key_3_fields_no_lsi_list.append(
                {"Subject": subject_key, "LastPostedBy": post_by})

    @task(10)
    def put_item_3_fields_1_lsi(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = random_name(20)
        post_by = random_name(20)

        resp = self.client.post(req_url,
                                qry.PUT_ITEM_3_FIELDS_1_LSI_RQ % (subject_key, post_by),
                                headers=qry.req_headers,
                                name="put_item")
        if resp.status_code == 200:
            key_3_fields_1_lsi_list.append({"Subject": subject_key, "LastPostedBy": post_by})

    @task(10)
    def put_item_10_fields_5_lsi(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = random_name(20)
        post_by = random_name(20)
        addtional_field_1 = random_name(20)
        addtional_field_2 = random_name(20)
        addtional_field_3 = random_name(20)
        addtional_field_4 = random_name(20)
        addtional_field_5 = random_name(20)
        addtional_field_6 = random_name(20)
        addtional_field_7 = random_name(20)

        resp = self.client.post(req_url,
                                qry.PUT_ITEM_10_FIELDS_5_LSI_RQ % (subject_key, post_by,
                                addtional_field_1, addtional_field_2, addtional_field_3,
                                addtional_field_4, addtional_field_5, addtional_field_6,
                                addtional_field_7),
                                headers=qry.req_headers,
                                name="put_item")
        if resp.status_code == 200:
            key_10_fields_5_lsi_list.append(
                {"Subject": subject_key,
                 "LastPostedBy": post_by,
                 "AdditionalField1": addtional_field_1,
                 "AdditionalField2": addtional_field_2,
                 "AdditionalField3": addtional_field_3,
                 "AdditionalField4": addtional_field_4})


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = cfg.MIN_WAIT
    max_wait = cfg.MAX_WAIT


# Master code
def on_slave_report(client_id, data):
    global IS_FIRST_RUN
    runner = locust.runners.locust_runner

    if IS_FIRST_RUN and runner.slave_count == cfg.SLAVE_COUNT:
        runner.start_hatching(cfg.LOCUST_COUNT, cfg.HATCH_RATE)
        IS_FIRST_RUN = False

    num_rq = sum([val.num_requests for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report


def create_table_helper(host, table_name, body):
    req_url = (host + '/v1/' +
               cfg.PROJECT_ID +
               '/data/tables/' + table_name)
    resp = requests.get(req_url, headers=qry.req_headers)
    if resp.status_code == 400 and "already exists" in resp.content:
        pass
    else:
        req_url = (host + '/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables')
        requests.post(req_url,
                      body,
                      headers=qry.req_headers)
        count = 0
        while count < 100:
            req_url = (host + '/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = requests.get(req_url, headers=qry.req_headers)
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                break
            else:
                count += 1
                time.sleep(1)
