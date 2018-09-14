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
export EDITOR=emacs
export CVS_EDITOR=emacs
export GIT_EDITOR=emacs
export SVN_EDITOR=emacs
