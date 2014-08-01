import sys
import queries as qry
import config as cfg
import requests
import json
import time


def main(host):
    print "Clean up ..."
    with open(qry.TABLE_LIST) as table_list_file:
        table_list = json.load(table_list_file)

        table_name_set = set(table_list['tables'])
        for table_name in table_name_set:
            req_url = (host + '/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = requests.get(req_url, headers=qry.req_headers)
            if resp.status_code != 200 or "DELETING" in resp.content:
                continue

            req_url = (host + '/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            requests.delete(req_url, headers=qry.req_headers)
            count = 0
            while count < 100:
                req_url = (host + '/v1/' +
                           cfg.PROJECT_ID +
                           '/data/tables/' + table_name)
                resp = requests.get(req_url, headers=qry.req_headers)
                if resp.status_code != 200:
                    print "deleted table %s" % table_name
                    break
                else:
                    time.sleep(1)
                count += 1
    print "Done."

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s host_url" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1])