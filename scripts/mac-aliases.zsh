alias ls="ls -CFG"
alias top="top -ocpu -R -F -s 2"
alias hub=git
alias vless="/opt/homebrew/share/vim/vim82/macros/less.sh"

function ql
{
    qlmanage -p "$@" >& /dev/null &
}

# Add a set of my SSH private keys to ssh-agent and also a keychain
function add-ssh-private-keys
{
    pgrep -U $(id -u) "ssh-agent" > /dev/null 2>&1
    if [[ $? != 0 ]]; then
        ssh-add -l -E md5 > /dev/null 2>&1
        ssh-add ${HOME}/.ssh/id_ed25519
        ssh-add --apple-load-keychain
    fi
}

function start-emacs-service
{
    if [[ "$(brew services list | grep "emacs-plus@27" | awk '{ print $2 }')" =~ stopped ]]; then
        brew services start emacs-plus@27 > /dev/null 2>&1
    fi
}

function stop-emacs-service
{
    if [[ "$(brew services list | grep "emacs-plus@27" | awk '{ print $2 }')" =~ started ]]; then
        brew services stop emacs-plus@27 > /dev/null 2>&1
    fi
}
