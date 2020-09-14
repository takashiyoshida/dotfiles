# Add project-related configurations or secrets here
# i.e. JIRA username, password
export JIRA_USER=""
export JIRA_PASS=""

NELARCHIVER_IP=$(grep "nelarchiver" /etc/hosts | awk '{ print $1 }')
export NELARCHIVER_IP

NELARCHIVER_PORT="80"
export NELARCHIVER_PORT
