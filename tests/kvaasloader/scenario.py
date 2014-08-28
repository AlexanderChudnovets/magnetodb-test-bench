import random
import string
import locust
from gevent import GreenletExit
from locust import task
import config as cfg
import queries as qry

MAX_EPOCH = 3333333333

PROJECT_ID = cfg.PROJECT_ID


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

    def put_item_kvaasloader(self):
        table_name = cfg.TABLE_NAME
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        id = self.random_name(20)
        created_date = random.randint(0, MAX_EPOCH)
        current_owner = self.random_name(20)
        deleted_date = random.randint(0, MAX_EPOCH)
        display_name = self.random_name(20)
        extension = self.random_name(20)
        file_type = self.random_name(20)
        last_access_date = random.randint(0, MAX_EPOCH)
        modified_date = random.randint(0, MAX_EPOCH)
        size = random.randint(0, MAX_EPOCH)
        path_id = self.random_name(20)
        msu_id = random.randint(0, MAX_EPOCH)
        tags = self.random_name(20)

        self.client.post(req_url,
                         qry.PUT_ITEM_KVAASLOADER_RQ % (id,
                                                        created_date,
                                                        current_owner,
                                                        deleted_date,
                                                        display_name,
                                                        extension,
                                                        file_type,
                                                        last_access_date,
                                                        modified_date,
                                                        size,
                                                        path_id,
                                                        msu_id,
                                                        tags),
                         headers=qry.req_headers,
                         name="put_item_kvaasloader")

    @task(10)
    def batch_write_item_kvaasloader(self):
        table_name = cfg.TABLE_NAME
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/batch_write_item')
        req_body = ''
        for i in xrange(cfg.BATCH_SIZE):
            id = self.random_name(20)
            created_date = random.randint(0, MAX_EPOCH)
            current_owner = self.random_name(20)
            deleted_date = random.randint(0, MAX_EPOCH)
            display_name = self.random_name(20)
            extension = self.random_name(20)
            file_type = self.random_name(20)
            last_access_date = random.randint(0, MAX_EPOCH)
            modified_date = random.randint(0, MAX_EPOCH)
            size = random.randint(0, MAX_EPOCH)
            path_id = self.random_name(20)
            msu_id = random.randint(0, MAX_EPOCH)
            tags = self.random_name(20)

            put_item_req = qry.PUT_ITEM_KVAASLOADER_RQ % (id,
                                                          created_date,
                                                          current_owner,
                                                          deleted_date,
                                                          display_name,
                                                          extension,
                                                          file_type,
                                                          last_access_date,
                                                          modified_date,
                                                          size,
                                                          path_id,
                                                          msu_id,
                                                          tags)
            req_body += ('{ "put_request": %s }' % put_item_req) if i == cfg.BATCH_SIZE - 1 else (
                '{ "put_request": %s }, ' % put_item_req)

        self.client.post(req_url,
                         qry.BATCH_WRITE_ITEM_KVAASLOADER_RQ % (table_name, req_body),
                         headers=qry.req_headers,
                         name="batch_write_item_kvaasloader")


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
