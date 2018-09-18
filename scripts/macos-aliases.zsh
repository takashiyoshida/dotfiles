alias top="top -ocpu -R -F -s 2"
alias hub=git
alias vless="/usr/local/share/vim/vim80/macros/less.sh"

function ql
{
    qlmanage -p "$@" >& /dev/null &
}
