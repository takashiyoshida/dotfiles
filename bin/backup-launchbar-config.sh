#!/bin/sh

# Backup the LaunchBar-related data to Dropbox (so I can reuse my snippets
# and other stuff in future).
# Use org.takashiyoshida.BackupLaunchBar.agent.plist to trigger the backup
# every hour automatically.
#
# `cp org.takashiyoshida.BackupLaunchBar.agent.plist ~/Library/LaunchAgents/`
# `launchctl load org.takashiyoshida.BackupLaunchBar.agent.plist`

LAUNCHBAR_DIR="${HOME}/Library/Application Support/LaunchBar"
DESTINATION_DIR="${HOME}/Dropbox/Apps"

BACKUP_DATE=`date "+%Y-%m-%d %H:%M"`
echo
echo "${BACKUP_DATE}: Backing up LaunchBar data..."
/usr/bin/rsync -avzh "${LAUNCHBAR_DIR}" "${DESTINATION_DIR}"
