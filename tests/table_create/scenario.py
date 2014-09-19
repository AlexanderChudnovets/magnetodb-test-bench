import random
import string
import locust
import time
import json
from gevent import GreenletExit
from locust.events import EventHook
from locust import task

import config as cfg
import ks_config as kscfg
import queries as qry

PROJECT_ID = kscfg.PROJECT_ID

table_name_set = set()


class UserBehavior(locust.TaskSet):
    def on_start(self):
        pass

    def on_stop(self):
        self.dump_tables_created()
        #self.delete_all_tables()

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

    def create_table_util(self, table_name, body, name):
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables')
        self.client.post(req_url, body, headers=kscfg.req_headers, name=name)

        while True:
            req_url = ('/v1/' +
                       PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=kscfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                table_name_set.add(table_name)
                break
            else:
                time.sleep(1)

    @task(1)
    def create_table_3_fields_no_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=kscfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               qry.CREATE_TABLE_3_FIELDS_NO_LSI_RQ % table_name,
                               "create_table_3_fields_no_lsi")

    @task(1)
    def create_table_10_fields_no_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=kscfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               qry.CREATE_TABLE_10_FIELDS_NO_LSI_RQ % table_name,
                               "create_table_10_fields_no_lsi")

    @task(3)
    def create_table_3_fields_1_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=kscfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               qry.CREATE_TABLE_3_FIELDS_1_LSI_RQ % table_name,
                               "create_table_3_fields_1_lsi")

    @task(5)
    def create_table_10_fields_5_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url,
                               headers=kscfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               qry.CREATE_TABLE_10_FIELDS_5_LSI_RQ % table_name,
                               "create_table_10_fields_5_lsi")

    def delete_table_util(self, table_name):
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name)
        self.client.delete(req_url,
                           headers=kscfg.req_headers,
                           name="delete_table")
        while True:
            req_url = ('/v1/' +
                       PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url,
                                   headers=kscfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200:
                table_name_set.discard(table_name)
                break
            else:
                time.sleep(1)

    def dump_tables_created(self):
        tables = {
            "tables": list(table_name_set)
        }
        with open(cfg.TABLE_LIST, 'w') as table_files:
            json.dump(tables, table_files)

    def delete_all_tables(self):
        for table_name in table_name_set:
            req_url = ('/v1/' +
                       PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=kscfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "DELETING" in resp.content:
                continue

            self.delete_table_util(table_name)


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

    num_rq = sum([val.num_requests for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report
