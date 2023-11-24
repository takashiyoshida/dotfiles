alias ls="eza --no-quotes"
alias ll="ls -l"
alias la="ls -a"
alias lll="ll --color=always | less"

# I actually want to have commands like these, but these commands can
# take very long time to execute.
# So I would rather not make it convenient to execute these commands.
# alias lsr="ls --tree"
# alias llr="ll --tree"

# Use btop instead
# alias top="top -ocpu -R -F -s 2"
alias hub=git
alias vless="/opt/homebrew/share/vim/vim90/macros/less.sh"

alias brout="brew update && brew outdated"
alias brupg="brew upgrade"

# For jekyll draft, post, publish, unpublish, page
alias jkld="jekyll draft"


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
