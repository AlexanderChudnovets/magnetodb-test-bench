import random
import locust
import time
import json
from gevent import GreenletExit
from locust.events import EventHook
from locust import task

import config as cfg
import ks_config as kscfg

PROJECT_ID = kscfg.PROJECT_ID

table_name_set = set()
table_3_fields_no_lsi_list = []
table_3_fields_1_lsi_list = []
table_10_fields_5_lsi_list = []


class UserBehavior(locust.TaskSet):
    def on_start(self):
        self.load_table_list()

    def on_stop(self):
        #self.delete_all_tables()
        pass

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
        global table_name_set

        with open(cfg.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_3_fields_no_lsi_list = table_list['table_3_fields_no_lsi']
            table_3_fields_1_lsi_list = table_list['table_3_fields_1_lsi']
            table_10_fields_5_lsi_list = table_list['table_10_fields_5_lsi']
        table_name_set |= set(table_3_fields_no_lsi_list)
        table_name_set |= set(table_3_fields_1_lsi_list)
        table_name_set |= set(table_10_fields_5_lsi_list)

    @task(1)
    def describe_table(self):
        if len(table_name_set) > 0:
            table_name = random.sample(table_name_set, 1)[0]
            req_url = ('/v1/' +
                       PROJECT_ID +
                       '/data/tables/' + table_name)
            self.client.get(req_url, headers=kscfg.req_headers,
                            name="describe_table")


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
