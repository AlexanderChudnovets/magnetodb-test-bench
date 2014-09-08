#!/bin/bash

### Version 1.2 2014.09.01.1740
### Developed by Alexei Vinogradov
### Mirantis, 2014


# Description
# -----------

# This script developed for clearing data of Cassandra and RRD logs.
# We should be logged as root.
# User root should be have ssh access without password to all nodes
# from ''CASSANDRA_NODE_LIST'' list and to ''RRD_NODE''.
# Script developed for Ubuntu 12.04.


# Variables
# ---------

# Specify IP address or hostname of all cassandra nodes. Separate via space.
CASSANDRA_NODE_LIST=${CASSANDRA_NODE_LIST:-"127.0.0.1"}

# Specify patterns or file names with full path of files of Cassandra. Separate via space.
# All files from this list will be erased.
CASSANDRA_FILES='/mnt/sdd1/cassandra/commitlog/* /mnt/sdb1_r0_4/cassandra/data/* /mnt/sdb1_r0_4/cassandra/saved_caches/*'

# The following variables are needed to create keyspace in Cassandra.
CASSANDRA_REPLICATION_STRATEGY='SimpleStrategy'
CASSANDRA_REPLICATION_FACTOR='3'

# Specify IP address or hostname of RRD node.
RRD_NODE='b0e015ash1001'

# Specify full path to directory with logs of RRD.
# All files from this directory will be erased.
RRD_LOG_DIR='/var/lib/collectd/rrd/*'


# ----------------------------------------------
MY_NAME=`basename "$0"`
MY_DIR=`pwd`
mkdir -p $MY_DIR/logs
MY_LOG=$MY_DIR/logs/$MY_NAME"_"`date +%F_%T`.log
# ----------------------------------------------


# Functions
# ---------

usage () {
  echo
  echo "usage: $MY_NAME [OPTIONS]"
  echo "Options:"
  echo "   -d    Erase all of data files of Cassandra specified in CASSANDRA_FILES variable."
  echo "   -l    Erase all of log files and dirs of RRD specified in RRD_LOG_DIR variable."
  echo
  echo "example: $MY_NAME -l -d"
  echo
  exit 1
}


function mydate {
  echo `date +%F%t%T%t`
}


myerror () {
  echo "$MY_NAME: During the execution occurred some error. Task fails." | tee -a $MY_LOG
  echo "$MY_NAME: See the log file $MY_LOG"
  exit 1
}


rr () { # Run remoutly
  echo "# ssh -tt $@" >> $MY_LOG
  ssh -tt $@ >> $MY_LOG 2>&1
  [ $? -ne 0 ] && myerror
}

check_node () {
  echo "# ssh -tt $1 :" >> $MY_LOG
  ssh -tt $1 : >> $MY_LOG 2>&1
  [ $? -ne 0 ] && echo "$MY_NAME: node $1 unreachable. Task fails." | tee -a $MY_LOG && exit 1
}


confirmation () {
  echo
  if [[ $CLEANUP_DATA == "true" ]]; then
      echo -n "On these nodes: "
      for i in ${CASSANDRA_NODE_LIST}; do
        echo -n "$i "
      done
      echo

      echo "Will be removed next files:"
      for i in ${CASSANDRA_FILES}; do
        echo $i
      done
      echo
  fi

  if [[ $CLEANUP_RRD == "true" ]]; then
      echo "On the node $RRD_NODE will be removed next files:"
      echo $RRD_LOG_DIR
      echo
  fi

  read -n 1 -p "You want to continue (y/n)?: " answer
  echo
  case "$answer" in
    [yY]) : ;;
    *)    echo "Operation canceled by user." ; exit 1 ;;
  esac
}


function create_keyspace_cassandra() {

  echo "SHOW HOST;" > $MY_DIR/cql.txt
  echo "CREATE KEYSPACE magnetodb WITH REPLICATION = { 'class' : '$CASSANDRA_REPLICATION_STRATEGY', 'replication_factor' : $CASSANDRA_REPLICATION_FACTOR };" >> $MY_DIR/cql.txt
  echo "CREATE KEYSPACE user_default_tenant WITH REPLICATION = { 'class' : '$CASSANDRA_REPLICATION_STRATEGY', 'replication_factor' : $CASSANDRA_REPLICATION_FACTOR };" >> $MY_DIR/cql.txt
  echo "CREATE TABLE magnetodb.table_info(tenant text, name text, exists int, \"schema\" text, status text, internal_name text, PRIMARY KEY(tenant, name));" >> $MY_DIR/cql.txt
  echo "exit;" >> $MY_DIR/cql.txt

  FIRST_NODE=`echo $CASSANDRA_NODE_LIST | cut -d' ' -f1`
  echo "# scp $MY_DIR/cql.txt $FIRST_NODE:/tmp/" >> $MY_LOG
  scp $MY_DIR/cql.txt $FIRST_NODE:/tmp/ >> $MY_LOG 2>&1
  [ $? -ne 0 ] && myerror

  echo | tee -a $MY_LOG
  echo "Waiting the cluster of Cassandra" | tee -a $MY_LOG
  timeout 120 sh -c "while ! nc -z ${FIRST_NODE} 9160; do echo -n '.'; sleep 1; done" || { echo; echo "Could not login at ${FIRST_NODE}:9160"; myerror; } && echo; rr $FIRST_NODE cqlsh -f /tmp/cql.txt ${FIRST_NODE} 9160
}


cleanup_cassandra () {
  echo | tee -a $MY_LOG
  for node_name in ${CASSANDRA_NODE_LIST}; do
    echo "Stoping Cassandra on $node_name" | tee -a $MY_LOG
    check_node $node_name
    rr $node_name service cassandra stop
  done

  for node_name in ${CASSANDRA_NODE_LIST}; do
    echo | tee -a $MY_LOG
    echo "Clearing data of cassandra on node $node_name:" | tee -a $MY_LOG
    for data_file in ${CASSANDRA_FILES}; do
      echo "    $data_file" | tee -a $MY_LOG
      rr $node_name rm -rf $data_file
    done
  done

  echo | tee -a $MY_LOG
  for node_name in ${CASSANDRA_NODE_LIST}; do
    echo "Starting Cassandra on $node_name" | tee -a $MY_LOG
    rr $node_name service cassandra start
  done

  create_keyspace_cassandra
}

cleanup_rrd () {
  echo | tee -a $MY_LOG
  echo "Stopting Collectd on $RRD_NODE" | tee -a $MY_LOG
  check_node $node_name
  rr $RRD_NODE service collectd stop

  echo "Clearing logs of RRD on node $RRD_NODE:" | tee -a $MY_LOG
  echo "    $RRD_LOG_DIR" | tee -a $MY_LOG
  rr $RRD_NODE rm -rf $RRD_LOG_DIR

  echo "Starting Collectd on $RRD_NODE" | tee -a $MY_LOG
  rr $RRD_NODE service collectd start
}


# Body
# ----

[[ $# -eq 0 ]] && usage

while getopts "dl" optname
  do
    case "$optname" in
      "d")
	CLEANUP_DATA="true"
        [[ x$CASSANDRA_FILES == "x" ]] && echo "Please specify CASSANDRA_FILES variable" && exit 1
        [[ x$CASSANDRA_NODE_LIST == "x" ]] && echo "Please specify CASSANDRA_NODE_LIST variable" && exit 1
        ;;
      "l")
        CLEANUP_RRD="true"
        [[ x$RRD_NODE == "x" ]] && echo "Please specify RRD_NODE variable" && exit 1
        [[ x$RRD_LOG_DIR == "x" ]] && echo "Please specify RRD_LOG_DIR variable" && exit 1
        RRD_LOG_DIR=`echo $RRD_LOG_DIR | sed 's/[/\*]*$/\/\*/'`
        ;;
      "?")
        echo "Unknown option $OPTARG"
	usage
        ;;
      *)
        echo "Unknown error while processing options"
	usage
        ;;
    esac
  done

confirmation

if [[ $CLEANUP_DATA == "true" ]]; then cleanup_cassandra; fi

if [[ $CLEANUP_RRD == "true" ]]; then cleanup_rrd; fi

echo
echo You can find log file at $MY_LOG
echo
echo Done.
echo
