import config as cfg
import json
import os.path

TOKEN = None
PROJECT_ID = None

if os.path.isfile(cfg.TOKEN_PROJECT):
    with open(cfg.TOKEN_PROJECT) as token_proj_file:
        token_project = json.load(token_proj_file)
        TOKEN = token_project['token'].strip()
        PROJECT_ID = token_project['project_id'].strip()

req_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Auth-Token': TOKEN
}
