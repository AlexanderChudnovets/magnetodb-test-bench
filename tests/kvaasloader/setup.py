import requests
import time
import queries as qry
import config as cfg


def create_table_helper(host, project_id, table_name, body):
    req_url = (host + '/v1/' +
               project_id +
               '/data/tables/' + table_name)
    resp = requests.get(req_url, headers=qry.req_headers)
    if resp.status_code == 400 and "already exists" in resp.content:
        pass
    else:
        req_url = (host + '/v1/' +
                   project_id +
                   '/data/tables')
        requests.post(req_url,
                      body,
                      headers=qry.req_headers)
        count = 0
        while count < 100:
            req_url = (host + '/v1/' +
                       project_id +
                       '/data/tables/' + table_name)
            resp = requests.get(req_url, headers=qry.req_headers)
            if resp.status_code != 200 or "ACTIVE" in resp.content:
                break
            else:
                count += 1
                time.sleep(1)


def setup(host):
    print("Initializing ...")
    token, project_id = cfg.TOKEN, cfg.PROJECT_ID

    create_table_helper(host, project_id, cfg.TABLE_NAME,
                        qry.CREATE_TABLE_KVAASLOADER_RQ % cfg.TABLE_NAME)

    print ("Done.")
