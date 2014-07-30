import random
import sys
import string
import time
import locust
from gevent import GreenletExit
from locust.events import EventHook
from locust import task
import requests

import config as cfg

IS_FIRST_RUN = True
MIN_WAIT = cfg.MIN_WAIT
MAX_WAIT = cfg.MAX_WAIT

subject_key_set = set()


class UserBehavior(locust.TaskSet):
    def on_start(self):
        pass
        # self.create_test_table()

    def on_stop(self):
        pass
        # self.delete_test_table()

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

    @task(5)
    def query(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/query')
        self.client.post(req_url, cfg.QUERY_TEST_TABLE_RQ, headers=cfg.req_headers, name="query")

    @task(5)
    def put_item(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/put_item')
        subject_key = self.random_name(20)

        resp = self.client.post(req_url, cfg.PUT_ITEM_TEST_TABLE_RQ % subject_key, headers=cfg.req_headers,
                                name="put_item")
        if resp.status_code == 200:
            subject_key_set.add(subject_key)

    @task(5)
    def delete_item(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/delete_item')
        if len(subject_key_set) > 0:
            subject_key = random.sample(subject_key_set, 1)[0]
            resp = self.client.post(req_url,
                                    cfg.DELETE_ITEM_TEST_TABLE_RQ % subject_key,
                                    headers=cfg.req_headers,
                                    name="delete_item")
            if resp.status_code == 200:
                subject_key_set.discard(subject_key)

    @task(10)
    def get_item(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/get_item')
        if len(subject_key_set) > 0:
            subject_key = random.sample(subject_key_set, 1)[0]
            self.client.post(req_url,
                             cfg.GET_ITEM_TEST_TABLE_RQ % subject_key,
                             headers=cfg.req_headers,
                             name="get_item")

    def create_table_util(self, table_name, body):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables')
        self.client.post(req_url, body, headers=cfg.req_headers, name="create_table")

        while True:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url,
                                   headers=cfg.req_headers,
                                   name="describe_table_helper_ignore")
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                break
            else:
                time.sleep(0.01)

    def create_test_table(self):
        table_name = cfg.TEST_TABLE_NAME
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url,
                               headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name, cfg.CREATE_TEST_TABLE_RQ)

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
                break
            else:
                time.sleep(0.01)

    def delete_test_table(self):
        table_name = cfg.TEST_TABLE_NAME
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = self.client.get(req_url,
                               headers=cfg.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code != 200 or "DELETING" in resp.content:
            return

        self.delete_table_util(table_name)


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

        table_name = cfg.TEST_TABLE_NAME
        req_url = (host + '/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = requests.get(req_url, headers=cfg.req_headers)
        if resp.status_code == 400 and "already exists" in resp.content:
            pass
        else:
            req_url = (host + '/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables')
            requests.post(req_url,
                          data=cfg.CREATE_TEST_TABLE_RQ,
                          headers=cfg.req_headers)
            count = 0
            while count < 100:
                req_url = (host + '/v1/' +
                           cfg.PROJECT_ID +
                           '/data/tables/' + table_name)
                resp = requests.get(req_url, headers=cfg.req_headers)
                if resp.status_code != 200 or "ACTIVE" in resp.content:
                    break
                else:
                    time.sleep(1)
                count += 1

    elif cmd == "end":
        print "Clean up ..."
        table_name = cfg.TEST_TABLE_NAME
        req_url = (host + '/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = requests.get(req_url, headers=cfg.req_headers)
        if resp.status_code != 200 or "DELETING" in resp.content:
            pass
        else:
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
