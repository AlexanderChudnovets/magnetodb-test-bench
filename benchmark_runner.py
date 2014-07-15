import datetime
import ConfigParser
import os
import re
import subprocess
import sys
import uuid

from fabric.operations import run, sudo, put
from fabric.context_managers import settings, prefix, cd


def change_rrd_dir(conf, rrd_dir):
    section_rx = re.compile(r'<Plugin rrdtool>([^<]*\n)*</Plugin>')
    section_mt = section_rx.search(conf)
    if not section_mt:
        raise Exception('There is no rrdtool section')

    section = section_mt.group()

    dir_rx = re.compile(r'DataDir\s+"[^"]*"')
    if dir_rx.search(section):
        result = dir_rx.sub('DataDir "%s"' % rrd_dir, section)
    else:
        result = section.replace('</Plugin>',
                                 '  DataDir "%s"\n</Plugin>' % rrd_dir)

    return section_rx.sub(result, conf)


def stop_monitoring():
    cmd = ['service', 'collectd', 'stop']
    subprocess.call(cmd, shell=False)


def start_monitoring():
    cmd = ['service', 'collectd', 'start']
    subprocess.call(cmd, shell=False)


def get_collectd_conf(conf_path='/etc/collectd/collectd.conf'):
    return open(conf_path, 'r').read()


def set_collectd_conf(conf, conf_path='/etc/collectd/collectd.conf'):
    open(conf_path, 'w').write(conf)


def start_load(cfg, locust_file):
    host = cfg.get('locust', 'host_to_test')
    requests_count = cfg.get('locust', 'requests_count')
    master_ip = cfg.get('locust', 'master_ip')
    master_port = cfg.get('locust', 'master_port')
    master_user = cfg.get('locust', 'master_user')
    master_password = cfg.get('locust', 'master_password')

    worker_ips = cfg.get('locust', 'worker_ips')
    if not worker_ips:
        # TODO: shutdown all
        sys.exit(-1)

    for slave_ip in worker_ips.split(','):
        slave_user = cfg.get(slave_ip, 'user')
        slave_password = cfg.get(slave_ip, 'password')
        start_locust_slave(slave_ip, slave_user, slave_password, locust_file, host, master_ip, master_port)

    start_locust_master(master_ip, master_port, master_user, master_password, locust_file, host, requests_count)


def runbg(cmd, sockname="dtach"):
    return run('dtach -n `mktemp -u /tmp/%s.XXXX` %s'  % (sockname, cmd))

def start_locust_master(master_ip, master_port, master_user, master_password, locust_file, host, requests_count):
    with (settings(host_string=master_ip, user=master_user, password=master_password)):
        with cd('locust'), prefix('source .venv/bin/activate'):
            cmd = 'locust -f %s -H %s --master -n %s --master-bind-host=%s --master-bind-port=%s'
            run(cmd % (locust_file, host, requests_count, master_ip, master_port))


def start_locust_slave(slave_ip, slave_user, slave_password, locust_file, host, master_ip, master_port):
    with (settings(host_string=slave_ip, user=slave_user, password=slave_password)):
        with cd('locust'), prefix('source .venv/bin/activate'):
            cmd = 'locust -f %s -H %s --no-web --slave --master-host=%s --master-port=%s'
            slave_locust_file = '/tmp/%s.py' % uuid.uuid4()
            put(locust_file, slave_locust_file)
            runbg(cmd % (slave_locust_file, host, master_ip, master_port))


def get_timestamp_str(timestamp=None):
    if timestamp:
        return timestamp.isoformat()
    return datetime.datetime.now().isoformat().replace('-', '_').replace('.', '_').replace(':', '_')
    

def store_results(results_dir):
    stop_monitoring()
    os.rename(results_dir, '%s_%s' % (results_dir,
        get_timestamp_str()))


def save_test_cfg(cfg_file, locust_file, results_dir):
    dst = os.path.join(results_dir, os.path.basename(cfg_file))
    cmd = ['cp', cfg_file, dst]
    print ' '.join(cmd)
    subprocess.call(cmd, shell=False)

    dst = os.path.join(results_dir, os.path.basename(locust_file))
    cmd = ['cp', locust_file, dst]
    print ' '.join(cmd)
    subprocess.call(cmd, shell=False)


def main(cfg_file, locust_file):
    cfg = ConfigParser.ConfigParser()
    cfg.read(cfg_file)

    base_dir =cfg.get('global', 'base_dir')
    prefix = cfg.get('global', 'result_dir_prefix')
    dir_name = '%s_%s' % (prefix, get_timestamp_str())
    results_dir = os.path.join(base_dir, dir_name)

    print ("Setup monitioring...")
    stop_monitoring()

    rrd_dir = os.path.join(results_dir, 'rrd')
    os.makedirs(rrd_dir)
    conf = get_collectd_conf()
    set_collectd_conf(change_rrd_dir(conf, rrd_dir))

    start_monitoring()
    
    print ("Start loading...")
    start_load(cfg, locust_file)

    save_test_cfg(cfg_file, locust_file, results_dir)

    print ("Saving results...")
    store_results(results_dir)

    print ("Done.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s /path/to/config.cfg /path/to/locust_file.py" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])
