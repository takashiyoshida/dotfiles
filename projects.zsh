# Work-related configurations

NIC="enp7s0"

if [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then

    function setup-nelarchiver
    {
        NELARCHIVER_IP=$(grep "nelarchiver" /etc/hosts | awk '{ print $1 }')
        NELARCHIVER_PORT="80"

        if [ -z "${NELARCHIVER_IP}" ]; then
            # When not working from office, I will run a Docker container as a nelarchiver
            # Depending on your OS, you will need to change the network interface below
            NELARCHIVER_IP=$(ifconfig ${NIC} | grep --color=never "inet " | awk '{ print $2 }')
            NELARCHIVER_PORT="8080"
        fi
        export NELARCHIVER_IP
        export NELARCHIVER_PORT
    }

    # Configure nelarchiver for this Linux machine
    setup-nelarchiver

    function mkdev
    {
        workspace=${PWD}
        if [[ $# != 0 ]]; then
            workspace=$1
            if [ ! -d ${workspace} ]; then
                echo "${workspace} does not exist"
                return
            fi
        fi

        session_name=$(basename ${workspace})
        tmux has-session -t ${session_name} 2> /dev/null
        if [[ $? != 0 ]]; then
            tmux detach

            cd ${workspace}

            tmux new-session -s ${session_name} -n build -d
            tmux split-window -h -t build
            tmux select-pane -t :.1 # Move the focus to the pane 1 of the build window

            # Administrating test VM (i.e. install new packages, etc)
            tmux new-window -n admin

            # Split ATS window in half (one for running ATS and another for logs)
            tmux new-window -n ATS
            tmux split-window -h -t ATS
            tmux select-pane -t :.1 # Move the focus to pane 1 of the ATS window

            # Split CMS window in half (one for running CMS and another for logs)
            tmux new-window -n CMS
            tmux split-window -h -t CMS
            tmux select-pane -t :.1 # Move the focus to pane 1 of the CMS window

            # Split ECS window in half (one for running ECS and another for logs)
            tmux new-window -n ECS
            tmux split-window -h -t ECS
            tmux select-pane -t :.1 # Move the focus to pane 1 of the ECS window

            # Split NED window in half (one for running NED and another for logs)
            tmux new-window -n NED
            tmux split-window -h -t NED
            tmux select-pane -t :.1 # Move the focus to pane 1 of the NED window

            # Split SMS window in half (one for running SMS and another for logs)
            tmux new-window -n SMS
            tmux split-window -h -t SMS
            tmux select-pane -t :.1 # Move the focus to pane 1 of the SMS window

            # Split SIM window in half (one for running SIM and another for logs)
            tmux new-window -n SIM
            tmux split-window -h -t SIM
            tmux select-pane -t :.1 # Move the focus to pane 1 of the SIM window

            # Go back to the build window and select the first pane
            tmux select-window -t build
            tmux select-pane -t :.1
        fi
        tmux attach -t ${session_name}
    }

    alias mkdev.c755b="mkdev ${HOME}/Projects/c755b-dev"
fi
