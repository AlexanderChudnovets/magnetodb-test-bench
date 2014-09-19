import os
import json
import requests
from subprocess import Popen, PIPE, STDOUT
import config as cfg
import queries as qry


def get_token_project(keystone_url, user, password, domain_name, project_name):
    body = qry.GET_TOKEN_RQ % (domain_name, user, password, domain_name, project_name)
    resp = requests.post(keystone_url, body, headers=cfg.token_req_headers)
    if resp.status_code != 201:
        raise Exception("Unable to get Keystone token")
    token = resp.headers['X-Subject-Token']
    project_id = json.loads(resp.content)['token']['project']['id']
    with open(cfg.TOKEN_PROJECT, 'w') as token_proj:
        json.dump({"token": token, "project_id": project_id}, token_proj)
    return token, project_id


def cassandra_cleanup():
    if os.path.isfile(cfg.CASSANDRA_CLEANER):
        my_env = os.environ.copy()
        my_env['CASSANDRA_NODE_LIST'] = cfg.CASSANDRA_NODES
        p = Popen([cfg.CASSANDRA_CLEANER, '-d'], stdout=PIPE,
            stdin=PIPE, stderr=STDOUT, env=my_env)
        stdout = p.communicate(input='y')[0]
        print stdout


def setup(host, keystone_url, user, password, domain_name, project_name):
    print('Clean C*...')
    cassandra_cleanup()

    print("Initializing ...")
    token, project_id = get_token_project(keystone_url, user, password,
                                          domain_name, project_name)
    print ("Done.")
