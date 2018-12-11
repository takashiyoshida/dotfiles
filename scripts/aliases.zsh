# Set TERM to xterm-256color to avoid incorrect color from being used
# in tmux session
alias emacs="TERM=xterm-256color emacs -nw"
alias tailf="tail -f"
alias history="history -i"

alias svndiff="svn diff --diff-cmd /usr/bin/diff -x -w"
alias svnldiff="svndiff -r COMMITTED" # Show the last commit
alias svninfo="svn info --show-item=url"
alias cdpr="cd ${HOME}/Projects"

alias lh="ls -lh"

# Create a new standup notes with today's date
alias standup="emacs `date +%F-standup.md`"
# Ignore unversioned files from svn status
alias svnst="svn status -q"
alias env="env | sort"

# Remove emacs backup files
alias rmeb="find . -name \"*~\" -delete"

# OS X specific aliases
if [[ "${OSTYPE}" =~ darwin* ]]; then
    source "${DOTFILES}/mac-aliases.zsh"
else
    source "${DOTFILES}/linux-aliases.zsh"
fi

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

function NELdev
{
    tmux has-session -t NELdev 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach # Detach from the current session
        cd ${HOME}/Projects/NELdev
        tmux new-session -s NELdev -n servers -d
        # Split the window in half (two panes side by side)
        tmux split-window -h -p 50 -t NELdev
        # Split the left pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t NELdev:1.1
        # Split the right pane in half (two panes, top and bottom)
        tmux split-window -v -p 50 -t NELdev:1.3
        # Make the top left pane active
        tmux select-pane -t NELdev:1.1

        tmux new-window -n dev -n editor
        tmux split-window -h -p 50 -t NELdev:2
        tmux select-pane -t NELdev:2.1
    fi
    tmux attach -t NELdev
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

function rturep
{
    tmux has-session -t rturep 2>/dev/null
    if [ $? != 0 ]; then
        tmux detach
        cd ${HOME}/Projects/rturep-elk
        tmux new-session -s rturep -d

        tmux split-window -h -p 50 -t rturep
        tmux select-pane -t rturep:1.1

        if [[ "${OSTYPE}" =~ darwin* ]]; then
            tmux send-keys -t rturep:1.1 'docker-compose up' C-m
        else
            tmux send-keys -t rturep:1.1 'sudo docker-compose up' C-m
        fi
    fi
    tmux attach -t rturep
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
