import sys
import config as cfg
import queries as qry
import requests
import time


def main(host):
    print "Initializing ..."
    table_name = cfg.TEST_TABLE_NAME
    req_url = (host + '/v1/' +
               cfg.PROJECT_ID +
               '/data/tables/' + table_name)
    resp = requests.get(req_url, headers=qry.req_headers)
    if resp.status_code == 400 and "already exists" in resp.content:
        pass
    else:
        req_url = (host + '/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables')
        requests.post(req_url,
                      data=qry.CREATE_TEST_TABLE_RQ,
                      headers=qry.req_headers)
        count = 0
        while count < 100:
            req_url = (host + '/v1/' +
                       cfg.PROJECT_ID +
                       '/data/tables/' + table_name)
            resp = requests.get(req_url, headers=qry.req_headers)
            if resp.status_code != 200 or "ACTIVE" in resp.content:
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