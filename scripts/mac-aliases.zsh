# alias ls="ls -CFG"
alias ls="exa -F --icons"
alias ll="exa -lF --icons"
alias la="ll -a"
alias lll="ll | less"
alias llr="ll -R"

alias top="top -ocpu -R -F -s 2"
alias hub=git
alias vless="/opt/homebrew/share/vim/vim90/macros/less.sh"

alias brout="brew update && brew outdated"
alias brupg="brew upgrade"

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
    if [[ "$(brew services list | grep 'emacs-plus@27' | awk '{ print $2 }')" != "started" ]]; then
        brew services start emacs-plus@27
    fi
}

function stop-emacs-service
{
    if [[ "$(brew services list | grep 'emacs-plus@27' | awk '{ print $2 }')" =~ started ]]; then
        brew services stop emacs-plus@27
    fi
}

function fix-macos-open-with-menu
{
    /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user

    echo "Now, run \`killall Finder to complete the fix."
}
