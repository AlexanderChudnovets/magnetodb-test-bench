import os
import random
import string
import json
import time

import requests
from subprocess import Popen, PIPE, STDOUT

import config as cfg
import ks_config as kscfg
import queries as qry


def create_table_helper(host, project_id, table_name, body):
    req_url = (host + '/v1/' +
               project_id +
               '/data/tables/' + table_name)
    resp = requests.get(req_url, headers=kscfg.req_headers)
    if resp.status_code == 400 and "already exists" in resp.content:
        pass
    else:
        req_url = (host + '/v1/' +
                   project_id +
                   '/data/tables')
        requests.post(req_url,
                      body,
                      headers=kscfg.req_headers)
        count = 0
        while count < 100:
            req_url = (host + '/v1/' +
                       project_id +
                       '/data/tables/' + table_name)
            resp = requests.get(req_url, headers=kscfg.req_headers)
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                break
            else:
                count += 1
                time.sleep(1)
    print "created table %s" % table_name


def random_name(length):
    return ''.join(random.choice(string.lowercase + string.digits)
                   for i in range(length))


def create_tables(host, project_id,
                  table_3_fields_no_lsi_list,
                  table_3_fields_1_lsi_list,
                  table_10_fields_5_lsi_list):
    table_name = random_name(20)
    table_3_fields_no_lsi_list.append(table_name)
    create_table_helper(host, project_id, table_name,
                        qry.CREATE_TABLE_3_FIELDS_NO_LSI_RQ % table_name)
    table_name = random_name(20)
    table_3_fields_1_lsi_list.append(table_name)
    create_table_helper(host, project_id, table_name,
                        qry.CREATE_TABLE_3_FIELDS_1_LSI_RQ % table_name)
    table_name = random_name(20)
    table_10_fields_5_lsi_list.append(table_name)
    create_table_helper(host, project_id, table_name,
                        qry.CREATE_TABLE_10_FIELDS_5_LSI_RQ % table_name)
    # dump tables created
    tables = {
        "table_3_fields_no_lsi": table_3_fields_no_lsi_list,
        "table_3_fields_1_lsi": table_3_fields_1_lsi_list,
        "table_10_fields_5_lsi": table_10_fields_5_lsi_list
    }
    with open(cfg.TABLE_LIST, 'w') as table_files:
        json.dump(tables, table_files)


def put_item_3_fields_no_lsi(host, project_id, table_3_fields_no_lsi_list, key_3_fields_no_lsi_list):
    table_name = random.choice(table_3_fields_no_lsi_list)
    req_url = (host + '/v1/' +
               project_id +
               '/data/tables/' + table_name + '/put_item')
    subject_key = random_name(20)
    post_by = random_name(20)
    resp = requests.post(req_url,
                         qry.PUT_ITEM_3_FIELDS_NO_LSI_RQ % (subject_key, post_by),
                         headers=kscfg.req_headers)
    if resp.status_code == 200:
        key_3_fields_no_lsi_list.append(
            {"Subject": subject_key, "LastPostedBy": post_by})


def put_item_3_fields_1_lsi(host, project_id, table_3_fields_1_lsi_list, key_3_fields_1_lsi_list):
    table_name = random.choice(table_3_fields_1_lsi_list)
    req_url = (host + '/v1/' +
               project_id +
               '/data/tables/' + table_name + '/put_item')
    subject_key = random_name(20)
    post_by = random_name(20)

    resp = requests.post(req_url,
                         qry.PUT_ITEM_3_FIELDS_1_LSI_RQ % (subject_key, post_by),
                         headers=kscfg.req_headers)
    if resp.status_code == 200:
        key_3_fields_1_lsi_list.append(
            {"Subject": subject_key, "LastPostedBy": post_by})


def put_item_10_fields_5_lsi(host, project_id, table_10_fields_5_lsi_list, key_10_fields_5_lsi_list):
    table_name = random.choice(table_10_fields_5_lsi_list)
    req_url = (host + '/v1/' +
               project_id +
               '/data/tables/' + table_name + '/put_item')
    subject_key = random_name(20)
    post_by = random_name(20)
    addtional_field_1 = random_name(20)
    addtional_field_2 = random_name(20)
    addtional_field_3 = random_name(20)
    addtional_field_4 = random_name(20)
    addtional_field_5 = random_name(20)
    addtional_field_6 = random_name(20)
    addtional_field_7 = random_name(20)

    resp = requests.post(req_url,
                         qry.PUT_ITEM_10_FIELDS_5_LSI_RQ % (subject_key, post_by,
                         addtional_field_1, addtional_field_2, addtional_field_3,
                         addtional_field_4, addtional_field_5, addtional_field_6,
                         addtional_field_7),
                         headers=kscfg.req_headers)
    if resp.status_code == 200:
        key_10_fields_5_lsi_list.append(
            {"Subject": subject_key,
             "LastPostedBy": post_by,
             "AdditionalField1": addtional_field_1,
             "AdditionalField2": addtional_field_2,
             "AdditionalField3": addtional_field_3,
             "AdditionalField4": addtional_field_4})


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

    kscfg.TOKEN = token
    kscfg.PROJECT_ID = project_id
    kscfg.req_headers['X-Auth-Token'] = token

    table_3_fields_no_lsi_list = []
    table_3_fields_1_lsi_list = []
    table_10_fields_5_lsi_list = []
    create_tables(host, project_id,
                  table_3_fields_no_lsi_list,
                  table_3_fields_1_lsi_list,
                  table_10_fields_5_lsi_list)

    key_3_fields_no_lsi_list = []
    key_3_fields_1_lsi_list = []
    key_10_fields_5_lsi_list = []

    for i in xrange(cfg.ROWS_POPULATED):
        put_item_3_fields_no_lsi(host, project_id,
                                 table_3_fields_no_lsi_list,
                                 key_3_fields_no_lsi_list)

        put_item_3_fields_1_lsi(host, project_id,
                                table_3_fields_1_lsi_list,
                                key_3_fields_1_lsi_list)

        put_item_10_fields_5_lsi(host, project_id,
                                 table_10_fields_5_lsi_list,
                                 key_10_fields_5_lsi_list)
    print "populated %d rows into each table" % cfg.ROWS_POPULATED
    keys = {
        "key_3_fields_no_lsi": key_3_fields_no_lsi_list,
        "key_3_fields_1_lsi": key_3_fields_1_lsi_list,
        "key_10_fields_5_lsi": key_10_fields_5_lsi_list
    }
    with open(cfg.ITEM_KEY_LIST, 'w') as item_files:
        json.dump(keys, item_files)

    print ("Done.")
