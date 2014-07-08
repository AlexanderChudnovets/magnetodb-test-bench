to run master:

locust -f magnetodb.py -H http://192.168.56.101:8480 --master -n 1000

to run slave:

locust -f magnetodb.py -H http://192.168.56.101:8480 --no-web --slave
