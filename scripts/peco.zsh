function exists { which $1 &> /dev/null }


function peco-src() {
    local src=$(ghq list --full-path | peco --query "$LBUFFER")
    if [ -n "${src}" ]; then
		BUFFER="cd ${src}"
		zle accept-line
    fi
    zle -R -c
}
zle -N peco-src
bindkey '^]' peco-src


function peco-select-history() {
    local tac
    exists gtac && tac="gtac" || { exists tac && tac="tac" || { tac="tail -r" }}
    BUFFER=$(fc -l -n 1 | eval ${tac} | peco --query "$LBUFFER")
    CURSOR=$#BUFFER
    zle -R -c
}
zle -N peco-select-history
bindkey '^R' peco-select-history


function peco-select-project() {
	local src=$(find ${HOME}/Projects -type d -d 1 | peco --query "$LBUFFER")
	if [ -n "${src}" ]; then
		BUFFER="cd ${src}"
		zle accept-line
	fi
	zle -R -c
}
zle -N peco-select-project
bindkey '^Y' peco-select-project


function ppgrep() {
    if [[ $1 == "" ]]; then
        PECO=peco
    else
        PECO="peco --query $1"
    fi
    ps xc -o user -o pid -o %cpu -o vsz -o rss -o start -o time -o comm | eval ${PECO} | awk '{ print $2 }'
}


function ppkill() {
    if [[ $1 =~ "^~" ]]; then
        QUERY="" # options only
    else
        QUERY=$1 # with a query
        [[ $# > 0 ]] && shift
    fi
    ppgrep ${QUERY} | xargs kill $*
}
