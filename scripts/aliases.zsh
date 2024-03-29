# Set the OS specific aliases first, then string together other aliases the build on them
if [[ "${OSTYPE}" =~ "darwin"* ]]; then
    source "${DOTFILES}/scripts/mac-aliases.zsh"
elif [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
    source "${DOTFILES}/scripts/linux-aliases.zsh"
fi

# Common set of aliases
alias mv="mv -i"
alias cp="cp -i"
alias rm="rm -i"

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

alias rake="noglob rake"

# Set TERM to xterm-256color to avoid incorrect color from being used
# in tmux session
alias tailf="tail -f"
alias history="history -i"

alias cdpr="cd ${HOME}/Projects"
alias senv="env | sort"

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
