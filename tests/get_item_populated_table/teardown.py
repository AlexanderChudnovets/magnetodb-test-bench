import json
import time

import requests

import ks_config as kscfg
import config as cfg


def cleanup(host):
    print "Clean up ..."
    with open(cfg.TABLE_LIST) as table_list_file:
        table_list = json.load(table_list_file)

        table_types = table_list.keys()
        for table_type in table_types:
            table_name_set = table_list[table_type]
            for table_name in table_name_set:
                req_url = (host + '/v1/' +
                           kscfg.PROJECT_ID +
                           '/data/tables/' + table_name)
                resp = requests.get(req_url, headers=kscfg.req_headers)
                if resp.status_code != 200 or "DELETING" in resp.content:
                    continue

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
