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

# Remove emacs backup files
alias rmeb="find . -name \"*~\" -delete"

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

function c755b-dev
{
    tmux has-session -t c755b 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach # Detach from the current session
        cd ${HOME}/Projects/c755b-dev
        tmux new-session -s c755b -n servers -d
        # Split the window in half (two panes side by side)
        tmux split-window -h -p 50 -t c755b
        # Split the left pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t c755b:1.1
        # Split the right pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t c755b:1.3
        # Make the top left pane active
        tmux select-pane -t c755b:1.1

        tmux new-window -n dev -n editor
        tmux split-window -h -p 50 -t c755b:2
        tmux select-pane -t c755b:2.1
    fi
    tmux attach -t c755b
}

function rturep-dev
{
    tmux has-session -t rturep 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach # Detach from the current session
        cd ${HOME}/Projects/rturep-dev
        tmux new-session -s rturep -n servers -d
        # Split the window in half (two panes side by side)
        tmux split-window -h -p 50 -t rturep
        # Split the left pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t rturep:1.1
        # Split the right pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t rturep:1.3
        # Make the top left pane active
        tmux select-pane -t rturep:1.1

        tmux new-window -n dev -n editor
        tmux split-window -h -p 50 -t rturep:2
        tmux select-pane -t rturep:2.1
    fi
    tmux attach -t rturep
}

function dotfiles
{
    tmux has-session -t dotfiles 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Projects/dotfiles
        tmux new-session -s dotfiles -d

        tmux split-window -h -p 50 -t dotfiles
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
