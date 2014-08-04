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

table_10_fields_5_lsi_list = []
key_10_fields_5_lsi_list = []
PROJECT_ID = qry.PROJECT_ID


class UserBehavior(locust.TaskSet):

    def on_start(self):
        self.load_table_list()

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
        global table_10_fields_5_lsi_list

        with open(qry.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_10_fields_5_lsi_list = table_list['table_10_fields_5_lsi']

    @task(10)
    def put_item_10_fields_5_lsi(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = self.random_name(20)
        post_by = self.random_name(20)
        addtional_field_1 = self.random_name(20)
        addtional_field_2 = self.random_name(20)
        addtional_field_3 = self.random_name(20)
        addtional_field_4 = self.random_name(20)
        addtional_field_5 = self.random_name(20)
        addtional_field_6 = self.random_name(20)
        addtional_field_7 = self.random_name(20)

        resp = self.client.post(req_url,
                                qry.PUT_ITEM_10_FIELDS_5_LSI_RQ % (subject_key, post_by,
                                addtional_field_1, addtional_field_2, addtional_field_3,
                                addtional_field_4, addtional_field_5, addtional_field_6,
                                addtional_field_7),
                                headers=qry.req_headers,
                                name="put_item_10_fields_5_lsi")
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
