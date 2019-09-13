# Go
export GOPATH="${HOME}/Projects"

# PATH
PATH="/usr/local/bin:/usr/local/sbin"
PATH="${PATH}:/usr/bin:/usr/sbin"
PATH="${PATH}:/bin:/sbin"

# Not sure about /usr/local/go/bin in non-macOS environment
PATH="${PATH}:/usr/local/go/bin"
PATH="${PATH}:${GOPATH}/bin"

if [[ "${OSTYPE}" =~ darwin* ]]; then
    # Installed by MacTex
    PATH="${PATH}:/usr/local/texlive/2018/bin/x86_64-darwin"
fi

PATH="${PATH}:${HOME}/bin"
PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
export PATH

if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi

if which rbenv > /dev/null; then
    eval "$(rbenv init -)"
fi

if which nodenv > /dev/null; then
    export PATH="${HOME}/.nodenv/bin:${PATH}"
    eval "$(nodenv init -)"
fi

if [ -f ${HOME}/.cargo/env ]; then
    source ${HOME}/.cargo/env
fi

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="UTF-8"
export LANG="en_US.UTF-8"

# Homebrew access token
# TODO: Assign your own access token
export HOMEBREW_GITHUB_API_TOKEN=""

# EDITOR
# CVS_EDITOR
# GIT_EDITOR
# SVN_EDITOR
export EDITOR="TERM=xterm-256color emacs -nw"
export CVS_EDITOR="TERM=xterm-256color emacs -nw"
export GIT_EDITOR="TERM=xterm-256color emacs -nw"
export SVN_EDITOR="TERM=xterm-256color emacs -nw"
