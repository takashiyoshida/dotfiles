# Set the OS specific aliases first, then string together other aliases the build on them
if [[ "${OSTYPE}" =~ darwin* ]]; then
    # OS X specific aliases
    source "${DOTFILES}/mac-aliases.zsh"
else
    # Linux specific aliases
    source "${DOTFILES}/linux-aliases.zsh"
fi

# Common set of aliases
alias lh="ls -lh"
alias lah="ls -lah"
alias lll="ll | less"

# Set TERM to xterm-256color to avoid incorrect color from being used
# in tmux session
alias tailf="tail -f"
alias history="history -i"

alias svndiff="svn diff --diff-cmd /usr/bin/diff -x -w"
alias svnldiff="svndiff -r COMMITTED" # Show the last commit
alias svninfo="svn info --show-item=url"
# Ignore unversioned files from svn status
alias svnst="svn status -q"

# For jekyll draft, post, publish, unpublish, page
alias jekyll="bundle exec jekyll"
alias jkld="jekyll draft"

alias cdpr="cd ${HOME}/Projects"
alias env="env | sort"

alias youtube-dl="youtube-dl --audio-quality 0 -o \"%(title)s-%(id)s.%(ext)s\""

alias e="emacsclient -c"
alias enw="emacsclient -c -nw"

alias df="df -H"

# Remove emacs backup files
alias rmeb="find . -name \"*~\" -delete"

# List fingerprints of SSH private keys
alias ls-idents="ssh-add -l -E md5"

# Send colored grep result to a pager (less)
alias grep="grep --color=always"

alias tree="tree -N"

# Add a set of my SSH private keys to ssh-agent and also a keychain
function add-ssh-private-keys
{
    ssh-add -l -E md5 > /dev/null 2>&1

    SSH_ADD_OPTION=""

    if [[ "${OSTYPE}" =~ darwin* ]]; then
        SSH_ADD_OPTION="-K"
    fi


    if [ $? != 0 ]; then
        ssh-add ${SSH_ADD_OPTION} ${HOME}/.ssh/digitalocean_rsa
        ssh-add ${SSH_ADD_OPTION} ${HOME}/.ssh/heroku_rsa
        ssh-add ${SSH_ADD_OPTION} ${HOME}/.ssh/takashi-thales_rsa
        ssh-add ${SSH_ADD_OPTION} ${HOME}/.ssh/github_rsa
        ssh-add ${SSH_ADD_OPTION} ${HOME}/.ssh/id_ed25519
    fi
}

# Useful functions to convert a hexadecimal number to a decimal number and vice versa
# http://www.cyberciti.biz/faq/linux-unix-convert-hex-to-decimal-number/
function h2d
{
    echo "ibase=16; $@" | bc
}

function d2h
{
    echo "obase=16; $@" | bc
}

function dirsize
{
    if [ -z "$@" ]; then
        MY_DIR=""
    else
        MY_DIR="$@"
    fi
    du -h -d 1 ${MY_DIR} | sort -h -r
}

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

alias mkdev.c755a="mkdev ${HOME}/Projects/c755a-dev"
alias mkdev.c755b="mkdev ${HOME}/Projects/c755b-dev"

function mkrturep
{
    workspace="${HOME}/Projects/rturep-dev"
    if [[ $# != 0 ]]; then
        workspace=$1
        if [ ! -d ${workspace} ]; then
            echo "${workspace} does not exist"
            return
        fi
    fi

    session_name=$(basename ${workspace})
    tmux has-session -t ${session_name} 2> /dev/null
    if [ $? != 0 ]; then
        tmux detach

        cd ${workspace}

        tmux new-session -s ${session_name} -n build -d
        tmux split-window -h -t build
        tmux select-pane -t :.1 # Move the focus to pane 1 of build window

        # Administrating test VM (i.e. install new packages, etc)
        tmux new-window -n admin

        # Split WLH window in half (one for running WLH and another for logs)
        tmux new-window -n WLH
        tmux split-window -h -t WLH
        tmux select-pane -t :.1 # Move the focus to pane 1 of the WLH window

        # Go back to the build window and select the first pane
        tmux select-window -t build
        tmux select-pane -t :.1
    fi
    tmux attach -t ${session_name}
}

function dotfiles
{
    tmux has-session -t dotfiles 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Projects/dotfiles
        tmux new-session -s dotfiles -d

        tmux split-window -h -t dotfiles
        tmux select-pane -t dotfiles:1.1
    fi
    tmux attach -t dotfiles
}

function rturep-elk
{
    tmux has-session -t rturep-elk 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Projects/rturep-elk
        tmux new-session -s rturep-elk -d

        tmux split-window -h -p 50 -t rturep-elk
        tmux select-pane -t rturep-elk:1.1

        if [[ "${OSTYPE}" =~ darwin* ]]; then
            tmux send-keys -t rturep-elk:1.1 'docker-compose up' C-m
        else
            tmux send-keys -t rturep-elk:1.1 'sudo docker-compose up' C-m
        fi
    fi
    tmux attach -t rturep-elk
}

function RTUtest
{
    tmux has-session -t RTUtest 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd /var/log
        tmux new-session -s RTUtest -n RTUtest -d
        tmux split-window -h -p 50 -t RTUtest
        tmux split-window -v -p 50 -t RTUtest:1.1
        tmux split-window -v -p 50 -t RTUtest:1.3

        tmux send-keys -t RTUtest:1.1 'top' C-m
        tmux select-pane -t RTUtest:1.1
    fi
    tmux attach -t RTUtest
}

function RTUreport
{
    tmux has-session -t RTUreport 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Documents/rturep/2\ Project\ Execution\ Data/2.2\ Work\ Products/04_Software/SprintReportsStatistics
        tmux new-session -s RTUreport -n RTUreport -d
        tmux split-window -h -p 50 -t RTUreport

        tmux select-pane -t RTUreport:1.1
        tmux send-keys -t RTUreport:1.1 'cd ${HOME}/Projects/dotfiles/bin' C-m
    fi
    tmux attach -t RTUreport
}

function standup
{
    tmux has-session -t standup 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Projects/standup
        tmux new-session -s standup -n standup -d
        tmux split-window -h -p 50 -t standup

        tmux select-pane -t standup:1.1
    fi
    tmux attach -t standup
}
