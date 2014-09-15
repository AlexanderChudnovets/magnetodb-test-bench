import json
import requests
import time
import queries as qry
import config as cfg


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


def setup(host, keystone_url, user, password, domain_name, project_name):
    print("Initializing ...")
    token, project_id = get_token_project(keystone_url, user, password,
                                          domain_name, project_name)

    create_table_helper(host, project_id, cfg.TABLE_NAME,
                        qry.CREATE_TABLE_KVAASLOADER_RQ % cfg.TABLE_NAME)

    print ("Done.")


def create_table_helper(host, project_id, table_name, body):
    import ks_config as kscfg
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
