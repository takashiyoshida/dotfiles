#!/usr/bin/env sh

# Convert existing AIFF files at Audio Hijack folder to FLAC format.
# Once the conversion is complete, the original AIFF files are deleted
# from disk.

TMP_LOG="/Users/takashi/Library/Logs/Backup/preflight.log"

SCRIPT=$0
SOURCE_DIR=$1
DESTINATION_DIR=$2

echo "Running ${SCRIPT} on $(/bin/date '+%B %d, %Y %H:%M:%S') ..." >> ${TMP_LOG}
echo "SOURCE_DIR: ${SOURCE_DIR}" >> ${TMP_LOG}
echo "DESTINATION_DIR: ${DESTINATION_DIR}" >> ${TMP_LOG}

(
    OIFS="${IFS}"
    IFS=$'\n'

    for src in $(/usr/bin/find "${SOURCE_DIR}/Audio Hijack" -name "*.aiff"); do
        dst="${src%.*}.flac"

        echo "Converting ${src} to a FLAC file, ${dst} ..." >> ${TMP_LOG}
        /opt/homebrew/bin/ffmpeg -y -i "${src}" "${dst}"
        if [[ $? == 0 ]]; then
            echo "Removing the original file, ${src} ..." >> ${TMP_LOG}
            rm -f "${src}"
        else
            echo "Failed to convert ${src} to a FLAC file ..." >> ${TMP_LOG}
        fi
    done

    IFS="${OIFS}"
)

echo "${SCRIPT} completed on $(/bin/date '+%B %d, %Y %H:%M:%S') ..." >> ${TMP_LOG}
