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
    # Installed by MacTex; 2019.0508 release works with macOS Catalina
    PATH="${PATH}:/usr/local/texlive/2019/bin/x86_64-darwin"
fi

PATH="${PATH}:${HOME}/bin"
PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
export PATH

if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi

if [[ "${OSTYPE}" =~ darwin* ]]; then
    # rbenv looks a bit old for Pop!_OS
    if which rbenv > /dev/null; then
        eval "$(rbenv init -)"
    fi
else
    PATH="${PATH}:${HOME}/.gem/ruby/2.5.0/bin"
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
export EDITOR="TERM=xterm-24bit emacsclient -c -t"
export CVS_EDITOR="TERM=xterm-24bit emacsclient -c -t"
export GIT_EDITOR="TERM=xterm-24bit emacsclient -c -t"
export SVN_EDITOR="TERM=xterm-24bit emacsclient -c -t"

if [[ "${OSTYPE}" =~ linux-gnu* ]]; then
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"
    export LD_LIBRARY_PATH
fi