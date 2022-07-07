NELARCHIVER_IP=$(grep "nelarchiver" /etc/hosts | awk '{ print $1 }')
NELARCHIVER_PORT="80"

if [ -z "${NELARCHIVER_IP}" ]; then
    # When not working from office, I will run a Docker container as a nelarchiver
    # Depending on your OS, you will need to change the network interface below
    NELARCHIVER_IP=$(ifconfig enp7s0 | grep --color=never "inet " | awk '{ print $2 }')
    NELARCHIVER_PORT="8080"
fi
export NELARCHIVER_IP
export NELARCHIVER_PORT

