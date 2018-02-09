#!/bin/bash

while IFS='' read -r server ; do
	count=0
	while [ "$count" -lt 30 ]; do
		traceroute $server
		echo "traceroute end"
		count=$((count+1))
	done
	echo "server end"
done < "$1"
