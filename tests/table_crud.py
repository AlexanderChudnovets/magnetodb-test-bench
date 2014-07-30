import random
import string
import sys
import locust
import time
import requests
import json
from gevent import GreenletExit
from locust.events import EventHook
from locust import task

import config as cfg

IS_FIRST_RUN = cfg.IS_FIRST_RUN
MIN_WAIT = 3000
MAX_WAIT = 10000

table_name_set = set()


class UserBehavior(locust.TaskSet):
    def on_start(self):
        pass

    def on_stop(self):
        # self.delete_all_tables()
        self.dump_tables_created()

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
                   cfg.PROJECT_ID +
                   '/data/tables')
        self.client.post(req_url, body, headers=cfg.req_headers, name=name)

        while True:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=cfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                table_name_set.add(table_name)
                break
            else:
                time.sleep(0.01)

    @task(1)
    def create_table_3_fields_no_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               cfg.CREATE_TABLE_3_fields_NO_LSI_RQ % table_name,
                               "create_table")

    @task(1)
    def create_table_10_fields_no_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               cfg.CREATE_TABLE_10_fields_NO_LSI_RQ % table_name,
                               "create_table")

    @task(3)
    def create_table_3_fields_1_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url, headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               cfg.CREATE_TABLE_3_fields_1_LSI_RQ % table_name,
                               "create_table")

    @task(5)
    def create_table_10_fields_5_lsi(self):
        table_name = self.random_name(20)

        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url,
                               headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name,
                               cfg.CREATE_TABLE_10_fields_5_LSI_RQ % table_name,
                               "create_table")

    def delete_table_util(self, table_name):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        self.client.delete(req_url,
                           headers=cfg.req_headers,
                           name="delete_table")
        while True:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url,
                                   headers=cfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200:
                table_name_set.discard(table_name)
                break
            else:
                time.sleep(1)

    @task(1)
    def delete_table(self):
        if len(table_name_set) > 0:
            table_name = random.sample(table_name_set, 1)[0]
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=cfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "DELETING" in resp.content:
                return

            self.delete_table_util(table_name)

    @task(10)
    def describe_table(self):
        if len(table_name_set) > 0:
            table_name = random.sample(table_name_set, 1)[0]
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            self.client.get(req_url, headers=cfg.req_headers,
                            name="describe_table")

    def dump_tables_created(self):
        tables = {
            "tables": list(table_name_set)
        }
        with open(cfg.TABLE_LIST, 'w') as table_files:
            json.dump(tables, table_files)

    def delete_all_tables(self):
        global table_name_set
        for table_name in table_name_set:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url, headers=cfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "DELETING" in resp.content:
                continue

            self.delete_table_util(table_name)
        table_name_set = set()


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = MIN_WAIT
    max_wait = MAX_WAIT


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


def main(host, cmd):
    if cmd == "start":
        print "Initializing ..."

    elif cmd == "end":
        print "Clean up ..."

        with open(cfg.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)

            table_name_set = set(table_list['tables'])
            for table_name in table_name_set:
                req_url = (host + '/v1/' +
                           cfg.PROJECT_ID +
                           '/data/tables/' + table_name)
                resp = requests.get(req_url, headers=cfg.req_headers)
                if resp.status_code != 200 or "DELETING" in resp.content:
                    continue

                req_url = (host + '/v1/' +
                           cfg.PROJECT_ID +
                           '/data/tables/' + table_name)
                requests.delete(req_url, headers=cfg.req_headers)
                count = 0
                while count < 100:
                    req_url = (host + '/v1/' +
                               cfg.PROJECT_ID +
                               '/data/tables/' + table_name)
                    resp = requests.get(req_url, headers=cfg.req_headers)
                    if resp.status_code != 200:
                        print "deleted table %s" %  table_name
                        break
                    else:
                        time.sleep(1)
                    count += 1

    else:
        print "Invalid command, exiting ..."
    print ("Done.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s host_url start|end" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])
