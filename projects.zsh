# Add project-related configurations or secrets here
# i.e. JIRA username, password
export JIRA_USER=""
export JIRA_PASS=""

NELARCHIVER_IP=$(grep "nelarchiver" /etc/hosts | awk '{ print $1 }')
NELARCHIVER_PORT="80"

if [ "${NELARCHIVER_IP}" != "" ]; then
    # When not working from office, I will run a Docker container as a nelarchiver
    NELARCHIVER_IP=$(ifconfig en0 | grep "inet " | awk '{ print $2 }')
    NELARCHIVER_PORT="8080"
fi
export NELARCHIVER_IP
export NELARCHIVER_PORT
