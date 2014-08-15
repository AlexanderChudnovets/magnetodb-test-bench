import json
import random
import string
import locust
from gevent import GreenletExit
from locust.events import EventHook
from locust import task

import config as cfg
import queries as qry


IS_FIRST_RUN = cfg.IS_FIRST_RUN

table_3_fields_1_lsi_list = []
key_3_fields_1_lsi_list = []

PROJECT_ID = qry.PROJECT_ID


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
        global table_3_fields_1_lsi_list

        with open(qry.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_3_fields_1_lsi_list = table_list['table_3_fields_1_lsi']

    def load_item_key_list(self):
        global key_3_fields_1_lsi_list

        with open(qry.ITEM_KEY_LIST) as item_key_list_file:
            item_key_list = json.load(item_key_list_file)
            key_3_fields_1_lsi_list = item_key_list['key_3_fields_1_lsi']

    @task(10)
    def get_item_3_fields_no_lsi(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/get_item')
        if len(key_3_fields_1_lsi_list) > 0:
            attribute_key = random.choice(key_3_fields_1_lsi_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url,
                             qry.GET_ITEM_3_FIELDS_NO_LSI_RQ % subject_key,
                             headers=qry.req_headers,
                             name="get_item_3_fields_no_lsi")


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
