# Set TERM to xterm-256color to avoid incorrect color from being used
# in tmux session
alias emacs="TERM=xterm-256color emacs -nw"
alias tailf="tail -f"
alias history="history -i"

alias svndiff="svn diff --diff-cmd /usr/bin/diff -x -w"
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
