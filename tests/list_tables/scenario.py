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

    @task(1)
    def list_tables(self):
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables')
        self.client.get(req_url, headers=kscfg.req_headers,
                        name="list_tables")

    @task(1)
    def list_tables_with_limit(self):
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables?limit=' + cfg.LIMIT)
        self.client.get(req_url, headers=kscfg.req_headers,
                        name="list_tables_with_limit_" + cfg.LIMIT)


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
