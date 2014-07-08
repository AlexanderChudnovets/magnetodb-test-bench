import collectd
import requests


def get_gauge(data):
    if not data:
        return 0
    if isinstance(data, float):
        return int(data)
    return data


def put_data(data):
    del(data['name'])
    for key in data:
        vl = collectd.Values(plugin='locust')
        vl.type = 'gauge'
        vl.type_instance = key
        vl.dispatch(values=[get_gauge(data[key])])


def write(vl, data=None):
    for i in vl.values:
        print "%s (%s): %f" % (vl.plugin, vl.type, i)


def read(data=None):
    rsp = requests.get('http://localhost:8089/stats/requests')
    data = rsp.json()

    if not data or ('stats' not in data):
        collectd.error('redis plugin: No info received')
        return

    for r in data['stats']:
        if r['name'] == 'Total':
            put_data(r)
        
collectd.register_read(read)
