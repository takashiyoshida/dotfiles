#!/usr/bin/env sh

TMP_LOG="/Users/takashi/Library/Logs/Backup/postflight.log"

SCRIPT=$0
SOURCE_DIR=$1
DESTINATION_DIR=$2

echo "Running ${SCRIPT} on $(/bin/date '+%B %d, %Y %H:%M:%S') ..." >> ${TMP_LOG}
echo "SOURCE_DIR: ${SOURCE_DIR}" >> ${TMP_LOG}
SOURCE_DIR="/System/Volumes/Data/Users/takashi/Music"
echo "Adjust the SOURCE_DIR to ${SOURCE_DIR} ..."
echo "DESTINATION_DIR: ${DESTINATION_DIR}" >> ${TMP_LOG}
echo "\$3: $3" >> ${TMP_LOG}
echo "\$4: $4" >> ${TMP_LOG}

(
    OIFS="${IFS}"
    IFS=$'\n'

    for src in $(/usr/bin/find "${SOURCE_DIR}/Audio Hijack" -name "*.flac"); do
        echo "Removing ${src} ..." >> ${TMP_LOG}
        rm -f "${src}"
    done

    for src in $(/usr/bin/find "${SOURCE_DIR}/GarageBand" -name "*.band"); do
        echo "Removing ${src} ..." >> ${TMP_LOG}
        rm -rf "${src}"
    done

    IFS="${OIFS}"
)

echo "${SCRIPT} completed on $(/bin/date '+%B %d, %Y %H:%M:%S') ..." >> ${TMP_LOG}
