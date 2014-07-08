import ConfigParser

import locust


cfg = ConfigParser.ConfigParser()
cfg.read('bench_runner.cfg')

first_run = False


class UserBehavior(locust.TaskSet):
    @locust.task
    def query(self):
        token = open('/home/alex/locust/token').read().strip()
        req_body = open('/home/alex/locust/query.json').read()
        req_url = ('/v1/e852b5ba507440fd99eee75593b3a35f'
                   '/data/tables/Thread/query')
        req_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': token
        }
        self.client.post(req_url, req_body, headers=req_headers)


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000


# Slave code
def on_report_to_master(client_id, data):
    global first_run
    
    if not first_run:
        data["first_run"] = 1
    first_run = True


# Master code
def on_slave_report(client_id, data):
    global first_run
    runner = locust.runners.locust_runner
    slave_count = cfg.getint('locust', 'slave_count')
    locust_count = cfg.getint('locust', 'locust_count')
    hatch_rate = cfg.getint('locust', 'hatch_rate')

    if (not first_run and slave_count and
            runner.slave_count == slave_count):
        runner.start_hatching(locust_count, hatch_rate)
        first_run = True


locust.events.report_to_master += on_report_to_master
locust.events.slave_report += on_slave_report
