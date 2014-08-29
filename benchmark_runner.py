import ConfigParser
import importlib
import sys

import re
import subprocess

import datetime
import os

from fabric.operations import run, sudo, put
from fabric.context_managers import settings, prefix, cd
import uuid

class BenchmarkRunner(object):
    def __init__(self, results_dir, cfg_file, cfg, benchmark, monitor):
        self.results_dir = results_dir
        self.benchmark = benchmark
        self.cfg_file = cfg_file
        self.cfg = cfg
        self.monitor = monitor

    def setup(self):
        self.benchmark.setup()

    def cleanup(self):
        self.benchmark.cleanup()

    def save_results(self):
        print "Store results"
        dst = os.path.join(self.results_dir, os.path.basename(self.cfg_file))
        cmd = ['cp', '-p', self.cfg_file, dst]
        subprocess.call(cmd, shell=False)

        src = os.path.basename(self.benchmark.__path__[0])
        dst = os.path.join(self.results_dir, src)
        cmd = ['cp', '-pr', self.benchmark.__path__[0], dst]
        subprocess.call(cmd, shell=False)

        res = '%s_%s' % (self.results_dir, get_timestamp())
        os.rename(self.results_dir, res)
        print 'Stored results in', res

    def start_loading(self):
        print "Start loading..."

    def run(self):
        self.setup()
        
        self.monitor.start()
        self.start_loading()
        self.monitor.stop()

        self.save_results()
        self.cleanup()


class LocustBenchmarkRunner(BenchmarkRunner):
    @staticmethod
    def runbg(cmd, sockname="dtach"):
        return sudo('dtach -n `mktemp -u /tmp/%s.XXXX` %s'  % (sockname, cmd))

    def start_slave(self, slave_ip, slave_user, slave_password, host, master_ip, master_port):
        with (settings(host_string=slave_ip, user=slave_user, password=slave_password)):
            cmd = 'locust -f %s/scenario.py -H %s --no-web --slave --master-host=%s --master-port=%s'
            slave_path = '/tmp/%s' % uuid.uuid4()
            run('mkdir -p %s' % slave_path)
            bm_path = self.benchmark.__path__[0]
            put(bm_path, slave_path)
            if slave_ip != master_ip:
                put(self.benchmark.config.TABLE_LIST, self.benchmark.config.TABLE_LIST)
            self.runbg(cmd % ('%s/%s' % (slave_path, self.benchmark.__name__.split('.')[-1]), host, master_ip, master_port))

    def start_master(self, master_ip, master_port, master_user, master_password, host, requests_count):
        with (settings(host_string=master_ip, user=master_user, password=master_password)):
            cmd = 'locust -f %s/scenario.py -H %s --master -n %s --master-bind-host=%s --master-bind-port=%s'
            sudo(cmd % (self.benchmark.__path__[0], host, requests_count, master_ip, master_port))

    def setup(self):
        
        host = self.cfg.get('locust', 'host_to_test')
        self.benchmark.setup(host)

        requests_count = self.cfg.get('locust', 'requests_count')
        master_ip = self.cfg.get('locust', 'master_ip')
        master_port = self.cfg.get('locust', 'master_port')
        master_user = self.cfg.get('locust', 'master_user')
        master_password = self.cfg.get('locust', 'master_password')
        requests_count = self.cfg.get('locust', 'requests_count')

        worker_ips = self.cfg.get('locust', 'worker_ips')
        for slave_ip in worker_ips.split(','):
            slave_user = self.cfg.get(slave_ip, 'user')
            slave_password = self.cfg.get(slave_ip, 'password')
            self.start_slave(slave_ip, slave_user, slave_password, host, master_ip, master_port)

    def start_loading(self):
        super(LocustBenchmarkRunner, self).start_loading()
        host = self.cfg.get('locust', 'host_to_test')
        requests_count = self.cfg.get('locust', 'requests_count')
        master_ip = self.cfg.get('locust', 'master_ip')
        master_port = self.cfg.get('locust', 'master_port')
        master_user = self.cfg.get('locust', 'master_user')
        master_password = self.cfg.get('locust', 'master_password')
        requests_count = self.cfg.get('locust', 'requests_count')
        self.start_master(master_ip, master_port, master_user, master_password, host, requests_count)

    def cleanup(self):
        host = self.cfg.get('locust', 'host_to_test')
        self.benchmark.cleanup(host)

class Monitor(object):
    def start(self):
        print "Start monitor"

    def stop(self):
        print "Stop monitor"


class CollectD(Monitor):
    def __init__(self, rrd_dir, orig_rrd_dir='/var/lib/collectd/rrd'):
        self.rrd_dir = rrd_dir
        self.orig_rrd_dir = orig_rrd_dir

    def _set_rrd_dir(self, rrd_dir, conf_file='/etc/collectd/collectd.conf'):
        with open(conf_file, 'r') as f:
            conf = f.read()
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
        with open(conf_file, 'w') as f:
            f.write(section_rx.sub(result, conf))

    def start(self):
        super(CollectD, self).start()
        cmd = ['service', 'collectd', 'stop']
        subprocess.call(cmd, shell=False)

        self._set_rrd_dir(self.rrd_dir)

        cmd = ['service', 'collectd', 'start']
        subprocess.call(cmd, shell=False)

    def stop(self):
        super(CollectD, self).stop()
        cmd = ['service', 'collectd', 'stop']
        subprocess.call(cmd, shell=False)

        self._set_rrd_dir(self.orig_rrd_dir)

        cmd = ['service', 'collectd', 'start']
        subprocess.call(cmd, shell=False)


def get_timestamp():
    return datetime.datetime.now().isoformat().replace('.', '_').replace(':', '_')


def main(conf_file, config, benchmark):

    base_dir = config.get('global', 'base_dir')
    prefix = config.get('global', 'result_dir_prefix')
    dir_name = '%s_%s' % (prefix, get_timestamp())
    results_dir = os.path.join(base_dir, dir_name)
    rrd_dir = os.path.join(results_dir, 'rrd')
    os.makedirs(rrd_dir)

    if config.get('global', 'monitor') == 'collectd':
        mon = CollectD(rrd_dir)
    if config.get('global', 'loader') == 'locust':
        runner = LocustBenchmarkRunner(results_dir, conf_file, config,
            benchmark, mon)
    runner.run()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s /path/to/config /path/to/benchmark" % sys.argv[0]
        sys.exit(-1)
    conf = ConfigParser.ConfigParser()
    conf.read(sys.argv[1])
    try:
        benchmark = importlib.import_module(sys.argv[2])
    except ImportError:
        print "Benchmark is not a python package"
        sys.exit(-1)
    main(sys.argv[1], conf, benchmark)
