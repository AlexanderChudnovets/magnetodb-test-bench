import locust


IS_FIRST_RUN = True
SLAVE_COUNT = 2
LOCUST_COUNT = 100
HATCH_RATE = 10

QUERY_RQ = """
{
    "key_conditions": {
        "ForumName": {                                                                                                   
            "attribute_value_list": [                                                                                  
                {                                                                                                    
                    "S": "MagnetoDB"
                }                                                                                                    
            ],                                                                                                       
            "comparison_operator": "EQ"
        }
    }
}
"""

TOKEN = """
MIIIAQYJKoZIhvcNAQcCoIIH8jCCB+4CAQExCTAHBgUrDgMCGjCCBlcGCSqGSIb3DQEHAaCCBkgEggZEeyJ0b2tlbiI6IHsibWV0aG9kcyI6IFsicGFzc3dvcmQiXSwgInJvbGVzIjogW3siaWQiOiAiYWVlNzBhM2ZlY2QyNGViZGFiZGZiN2NlZjNjNGNjNTEiLCAibmFtZSI6ICJNZW1iZXIifV0sICJleHBpcmVzX2F0IjogIjIwMTQtMDctMThUMTg6Mjg6MjYuMDcxMzc0WiIsICJwcm9qZWN0IjogeyJkb21haW4iOiB7ImlkIjogIjE0MDI2OGUxZjgzMzRkYmU4ZDc2OTM3MjcxYWIxMWEyIiwgIm5hbWUiOiAiZG9tYWluMSJ9LCAiaWQiOiAiZTg1MmI1YmE1MDc0NDBmZDk5ZWVlNzU1OTNiM2EzNWYiLCAibmFtZSI6ICJwcm9qZWN0MSJ9LCAiY2F0YWxvZyI6IFt7ImVuZHBvaW50cyI6IFt7InVybCI6ICJodHRwOi8vMTkyLjE2OC41Ni4xMDE6ODQ4MC92MS9lODUyYjViYTUwNzQ0MGZkOTllZWU3NTU5M2IzYTM1ZiIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVyZmFjZSI6ICJhZG1pbiIsICJpZCI6ICIxODYxYTFkYjk5ZWQ0NzZlODg5YzE1Y2IzYmNmMjBhYyJ9LCB7InVybCI6ICJodHRwOi8vMTkyLjE2OC41Ni4xMDE6ODQ4MC92MS9lODUyYjViYTUwNzQ0MGZkOTllZWU3NTU5M2IzYTM1ZiIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVyZmFjZSI6ICJwdWJsaWMiLCAiaWQiOiAiM2FiZjlkMGQzNzI2NGU5Mjg1NDU4MjFlZDU0NzIxOWUifSwgeyJ1cmwiOiAiaHR0cDovLzE5Mi4xNjguNTYuMTAxOjg0ODAvdjEvZTg1MmI1YmE1MDc0NDBmZDk5ZWVlNzU1OTNiM2EzNWYiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcmZhY2UiOiAiaW50ZXJuYWwiLCAiaWQiOiAiNTU0MDJjYTgwNmU3NGM2MDg2ZjIyYjFlMDZlMmZhODkifV0sICJ0eXBlIjogImt2LXN0b3JhZ2UiLCAiaWQiOiAiZTlmMmMzOWIxMDI5NDUwZWI4Y2RiZDZlZTZkMzk0ZjMiLCAibmFtZSI6ICJtYWduZXRvZGIifSwgeyJlbmRwb2ludHMiOiBbeyJ1cmwiOiAiaHR0cDovLzE5Mi4xNjguNTYuMTAxOjM1MzU3L3YyLjAiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcmZhY2UiOiAiYWRtaW4iLCAiaWQiOiAiMTRmYzAyNTY2YjQwNGFjNGI0YTc5OTk5MTlkNDZiYjcifSwgeyJ1cmwiOiAiaHR0cDovLzE5Mi4xNjguNTYuMTAxOjUwMDAvdjIuMCIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVyZmFjZSI6ICJpbnRlcm5hbCIsICJpZCI6ICIyMDEyMTdiMjJlMGY0NDc3OTg5ZTQ5Mzc1YzQzZTkxZSJ9LCB7InVybCI6ICJodHRwOi8vMTkyLjE2OC41Ni4xMDE6NTAwMC92Mi4wIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJmYWNlIjogInB1YmxpYyIsICJpZCI6ICI1NGEwMTdkZGQxZjg0ODQ2YjNmN2FkNzhmYjM4ZTI5YiJ9XSwgInR5cGUiOiAiaWRlbnRpdHkiLCAiaWQiOiAiZjlmOWY4NTEzMzkzNDllYWIxZGY4OGFkMTA4OTAzOWIiLCAibmFtZSI6ICJrZXlzdG9uZSJ9XSwgImV4dHJhcyI6IHt9LCAidXNlciI6IHsiZG9tYWluIjogeyJpZCI6ICIxNDAyNjhlMWY4MzM0ZGJlOGQ3NjkzNzI3MWFiMTFhMiIsICJuYW1lIjogImRvbWFpbjEifSwgImlkIjogImExMTMxMzA5Y2Y4MjRhMjY5MDIyNDExNmZlMjM2MjY1IiwgIm5hbWUiOiAidXNlcjEifSwgImlzc3VlZF9hdCI6ICIyMDE0LTA2LTE4VDE4OjI4OjI2LjA3MTQzMVoifX0xggGBMIIBfQIBATBcMFcxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIDAVVbnNldDEOMAwGA1UEBwwFVW5zZXQxDjAMBgNVBAoMBVVuc2V0MRgwFgYDVQQDDA93d3cuZXhhbXBsZS5jb20CAQEwBwYFKw4DAhowDQYJKoZIhvcNAQEBBQAEggEAhzdBEX+wTCNO0IXVtOkVoDjuk-TGZbq17s12WxczFg8pUIIwa+5jaXeIw9s6cfacP5tSs+7rghZz+ClXEsI8SIVrLroPJsp5uQMQmmHYKZhLbBnUL2xnhibaD8zTlzCn7ExXnP0lBQ5zMS78Z1tGwodj29DQfLGxsbzwYlk4yrdLT-vcRWpclpiQDCwV8ABBT4ME4jv7qWYSS229DNHAYui2Aponbln8Pe785XYOC01VipLW-BOAyZik1zdeVfuU2IIZjylLCgVibAY1-bnfFT6J0acGmeol+vbT1F+T1yPHLfHPmUUcx0dyJ8vcDktlM0CaJpPqNWGFQvxUtGOY6Q==
"""


class UserBehavior(locust.TaskSet):
    @locust.task
    def query(self):
        req_url = ('/v1/e852b5ba507440fd99eee75593b3a35f'
                   '/data/tables/Thread/query')
        req_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': TOKEN.strip()
        }
        self.client.post(req_url, QUERY_RQ.strip(), headers=req_headers)


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000


# Master code
def on_slave_report(client_id, data):
    global IS_FIRST_RUN
    runner = locust.runners.locust_runner

    if IS_FIRST_RUN and runner.slave_count == SLAVE_COUNT:
        runner.start_hatching(LOCUST_COUNT, HATCH_RATE)
        IS_FIRST_RUN = False

    num_rq = sum([val.num_requests for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report
