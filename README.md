=====
MagnetoDB testing tools
=====
Installation
--------
collectd

apt-get install collectd

locust

pip install locustio

grafite

# 0.9.x (stable) branch
git clone https://github.com/graphite-project/graphite-web.git
cd graphite-web
git checkout 0.9.x
cd ..
git clone https://github.com/graphite-project/carbon.git
cd carbon
git checkout 0.9.x
cd ..
git clone https://github.com/graphite-project/whisper.git
cd whisper
git checkout 0.9.x
cd ..


Install Whisper

pushd whisper
sudo python setup.py install
popd
Install Carbon

By default, everything will be installed in /opt/graphite

To install carbon:

pushd
python setup.py install 
popd
Configure Carbon

pushd /opt/graphite/conf
cp carbon.conf.example carbon.conf
cp storage-schemas.conf.example storage-schemas.conf



To run benchmark:

sudo python benchmark_runner.py /path/to/benchmark_runner.cfg /path/to/locust_file.py

Example:
sudo python benchmark_runner.py /home/alex/benchmark_runner.cfg /home/alex/locust/test_query.py

FIXME:
locust should be installed as package. I used venv in this script.

There are 8 test scenarios under tests. You need to change tests/config.py to use your project Id and Keystone token.

Some test cases are ordered. Test case ending with *_populated_table.py needs to run after the corresponding *_with_no_table.py is run, which will create and populate tables for it.

For each test scenario, follow the steps below:
1. python [my_test_scenario]/setup.py http://my_magnetodb_api_server:8480
2. run benchmark_runner as above
3. python [my_test_scenario]/teardown.py http://my_magnetodb_api_server:8480

These 3 steps will be integrated into benchmark_runner.py soon.