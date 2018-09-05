# OS X specific aliases
if [[ "${OSTYPE}" =~ darwin* ]]; then
    alias top="top -ocpu -R -F -s 2"
    alias hub=git
fi

# Set TERM to xterm-256color to avoid incorrect color from being used
# in tmux session
alias emacs="TERM=xterm-256color emacs -nw"
alias tailf="tail -f"
alias history="history -i"

alias svndiff="svn diff --diff-cmd /usr/bin/diff -x -w"
alias vless="/usr/local/share/vim/vim80/macros/less.sh"

alias cdpr="cd ${HOME}/Projects"

alias lh="ls -lh"

# OS X specifc functions
function ql
{
    qlmanage -p "$@" >& /dev/null &
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
