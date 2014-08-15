import sys
import json
import requests
import queries as qry


def get_token_project(keystone_url, user, password, domain_name, project_name):
    body = qry.GET_TOKEN_RQ % (domain_name, user, password, domain_name, project_name)
    resp = requests.post(keystone_url, body, headers=qry.token_req_headers)
    if resp.status_code != 201:
        raise Exception("Unable to get Keystone token")
    token = resp.headers['X-Subject-Token']
    project_id = json.loads(resp.content)['token']['project']['id']
    with open(qry.TOKEN_PROJECT, 'w') as token_proj:
        json.dump({"token": token, "project_id": project_id}, token_proj)
    return token, project_id


def main(host, keystone_url, user, password, domain_name, project_name):
    print("Initializing ...")
    get_token_project(keystone_url, user, password,
                      domain_name, project_name)

    print ("Done.")


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print "Usage: %s host_url keystone_url, user, password, domain_name, project_name" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])