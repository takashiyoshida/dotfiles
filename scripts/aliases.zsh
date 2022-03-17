# Set the OS specific aliases first, then string together other aliases the build on them
if [[ "${OSTYPE}" =~ darwin* ]]; then
    # OS X specific aliases
    source "${DOTFILES}/scripts/mac-aliases.zsh"
else
    # Linux specific aliases
    source "${DOTFILES}/scripts/linux-aliases.zsh"
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

alias mkdev.c755b="mkdev ${HOME}/Projects/c755b-dev"

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
