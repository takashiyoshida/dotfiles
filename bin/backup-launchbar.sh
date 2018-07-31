#!/bin/sh

# Backup the LaunchBar-related data to Dropbox (so I can reuse my snippets
# and other stuff in future).
# Use org.takashiyoshida.BackupLaunchBar.agent.plist to trigger the backup
# every hour automatically.
#
# `cp org.takashiyoshida.BackupLaunchBar.agent.plist ~/Library/LaunchAgents/`
# `launchctl load org.takashiyoshida.BackupLaunchBar.agent.plist`

RSYNC=/usr/bin/rsync
RSYNC_OPT="-avz"

LAUNCHBAR_PATH="${HOME}/Library/Application Support/LaunchBar/"
DESTINATION_PATH="${HOME}/Dropbox/Documents/LaunchBar"

BACKUP_DATE=`date "+%Y-%m-%d %H:%M:%S"`

echo
echo "${BACKUP_DATE}: Backing up LaunchBar data..."
${RSYNC} ${RSYNC_OPT} "${LAUNCHBAR_PATH}" "${DESTINATION_PATH}"
