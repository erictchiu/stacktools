#!/bin/bash

# TODO : parameterize the input directory, otherwise we may overwrite wrong version

cd /root/tripleo/tripleo-incubator/scripts 

# restore seed
./hp_ced_restore.sh -S -f /root/backup/backup_14-11-01-00-11 -c /root/baremetal.csv

# restore undercloud
./hp_ced_restore.sh -U -f /root/backup/backup_14-11-01-00-15 -c /root/baremetal.csv

# restore overcloud
./hp_ced_restore.sh -O -f /root/backup/backup_14-11-01-00-36

