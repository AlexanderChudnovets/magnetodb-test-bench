import random
import string
import time
import locust
from gevent import GreenletExit
from locust.events import EventHook
from locust import task

import config as cfg
import queries as qry


IS_FIRST_RUN = True

subject_key_set = set()


class UserBehavior(locust.TaskSet):
    def on_start(self):
        pass

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

    @task(5)
    def query(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/query')
        self.client.post(req_url, qry.QUERY_TEST_TABLE_RQ, headers=qry.req_headers, name="query")

    @task(5)
    def put_item(self):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + cfg.TEST_TABLE_NAME + '/put_item')
        subject_key = self.random_name(20)

        resp = self.client.post(req_url, qry.PUT_ITEM_TEST_TABLE_RQ % subject_key, headers=qry.req_headers,
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
                                    qry.DELETE_ITEM_TEST_TABLE_RQ % subject_key,
                                    headers=qry.req_headers,
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
                             qry.GET_ITEM_TEST_TABLE_RQ % subject_key,
                             headers=qry.req_headers,
                             name="get_item")

    def create_table_util(self, table_name, body):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables')
        self.client.post(req_url, body, headers=qry.req_headers, name="create_table")

        while True:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url,
                                   headers=qry.req_headers,
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
                               headers=qry.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code == 400 and "already exists" in resp.content:
            return
        self.create_table_util(table_name, qry.CREATE_TEST_TABLE_RQ)

    def delete_table_util(self, table_name):
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        self.client.delete(req_url,
                           headers=qry.req_headers,
                           name="delete_table")
        while True:
            req_url = ('/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = self.client.get(req_url,
                                   headers=qry.req_headers,
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
                               headers=qry.req_headers,
                               name="describe_table_helper_ignore")
        if resp.status_code != 200 or "DELETING" in resp.content:
            return

        self.delete_table_util(table_name)


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
