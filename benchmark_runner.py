import datetime
import os
import re
import subprocess


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


def start_load():
    # Run loading tool here
    # Simulate test run for now
    import time
    import random
    time.sleep(random.randrange(60, 180))


def get_timestamp_str(timestamp=None):
    if timestamp:
        return timestamp.isoformat()
    return datetime.datetime.now().isoformat()
    

def store_results(results_dir):
    stop_monitoring()
    os.rename(results_dir, '%s_%s' % (results_dir,
        get_timestamp_str()))

def run_bench(results_dir):
    print ("Setup monitioring...")
    stop_monitoring()
    
    rrd_dir = os.path.join(results_dir, 'rrd')
    os.makedirs(rrd_dir)
    conf = get_collectd_conf()
    set_collectd_conf(change_rrd_dir(conf, rrd_dir))

    start_monitoring()
    
    print ("Start loading...")
    start_load()

    print ("Saving results...")
    store_results(results_dir)

    print ("Done.")


def main():
    base_dir = '/home/alex'
    dir_name = 'test_%s' % get_timestamp_str()
    run_bench(os.path.join(base_dir, dir_name))


if __name__ == '__main__':
    main()
