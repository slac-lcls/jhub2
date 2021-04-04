#!/bin/bash 
#
# Print active jhub users
#
# Usage:
#        user_status.sh [-h]
# Options:
#    -h:  print this help  
#

set -u

active_users() {
    sqlite3 ${DB} \
	"select u.name,sv.ip,sp.state,sp.started,sp.last_activity from spawners sp, users u, servers sv \
	where sp.server_id is NOT NULL and sp.user_id=u.id and sp.server_id=sv.id; "
}


if [[ $# -ge 1 && ${1} = '-h' ]] ; then
    sed -n -e '2,/^[^#]\|^$/ s/^#//p' $0
    exit
fi


DB="jupyterhub.sqlite"

active_users
