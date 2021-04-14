alias ls="ls -CFG"
alias top="top -ocpu -R -F -s 2"
alias hub=git
alias vless="/opt/homebrew/share/vim/vim82/macros/less.sh"

function ql
{
    qlmanage -p "$@" >& /dev/null &
}
