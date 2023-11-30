#!/usr/bin/env bash

# Returns 1 when Carbon Copy Cloner is performing a backup task,
# otherwise returns 0.
#
# Bartender shows Carbon Copy Cloner icon in the menu when
# Carbon Copy Cloner performs backup.

CCC="/Applications/Carbon Copy Cloner.app/Contents/MacOS/ccc"

result=0
for state in $("${CCC}" --status | awk -F '|' '{ print $2 }'); do
	if [[ "${state}" == "running" ]]; then
		result=1
		break
	fi
done
echo "${result}"
