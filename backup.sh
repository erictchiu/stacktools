#!/bin/bash

export BRIDGE_INTERFACE=em3
export OVERCLOUD_NTP_SERVER=15.126.25.4
export UNDERCLOUD_NTP_SERVER=15.126.25.4
export OVERCLOUD_CODN_HTTP_PROXY=http://web-proxy.useast.hpcloud.net:8080
export OVERCLOUD_CODN_HTTPS_PROXY=https://web-proxy.useast.hpcloud.net:8080
export UNDERCLOUD_CODN_HTTP_PROXY=http://web-proxy.useast.hpcloud.net:8080
export UNDERCLOUD_CODN_HTTPS_PROXY=https://web-proxy.useast.hpcloud.net:8080

cd /root/tripleo/tripleo-incubator/scripts/
./hp_ced_backup.sh --seed -f /root/backup
./hp_ced_backup.sh --undercloud -f /root/backup
./hp_ced_backup.sh --overcloud -f /root/backup
