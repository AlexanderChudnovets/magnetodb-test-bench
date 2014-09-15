import requests
import time

import config as cfg
import ks_config as kscfg


def cleanup(host):
    print "Clean up ..."
    table_name = cfg.TABLE_NAME
    req_url = (host + '/v1/' +
               kscfg.PROJECT_ID +
               '/data/tables/' + table_name)
    resp = requests.get(req_url, headers=kscfg.req_headers)
    if resp.status_code == 200 and "DELETING" not in resp.content:
        req_url = (host + '/v1/' +
                   kscfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        requests.delete(req_url, headers=kscfg.req_headers)
    count = 0
    while count < 100:
        req_url = (host + '/v1/' +
                   kscfg.PROJECT_ID +
                   '/data/tables/' + table_name)
        resp = requests.get(req_url, headers=kscfg.req_headers)
        if resp.status_code != 200:
            print "deleted table %s" % table_name
            break
        else:
            time.sleep(1)
        count += 1
    print "Done."
