# Configure PATH variable
# Default PATH (macOS Big Sur)
# PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin
# - /usr/local/bin
# - /usr/bin
# - /bin
# - /usr/sbin
# - /sbin
# - /Library/Apple/usr/bin

if [[ "${OSTYPE}" =~ darwin* ]]; then
    # MacTex (brew install --cask mactex) is a Universal binary package
    PATH="${PATH}:/usr/local/texlive/2021/bin/universal-darwin"

    # Add Homebrew path (/opt/homebrew/bin) to PATH
    eval "$(/opt/homebrew/bin/brew shellenv)"
    # For some reason, my MacBook Pro 14" does not do tab-completion for
    # Homebrew so this allows the tab-completion to work.
    if type brew >/dev/null 2>&1; then
        FPATH=$(brew --prefix)/completions/zsh:${FPATH}
        autoload -Uz compinit
        compinit
    fi

    # Building Python via pyenv install...
    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix bzip2)/include"
    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix zlib)/include"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix bzip2)/lib"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix bzip2)/lib"
fi

# Configure LD_LIBRARY_PATH
if [[ "${OSTYPE}" =~ linux-gnu* ]]; then
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"
    export LD_LIBRARY_PATH

    # rbenv looks a bit old for Pop!_OS
    PATH="${PATH}:${HOME}/.gem/ruby/2.5.0/bin"
fi

if which pyenv > /dev/null; then
    export PYENV_ROOT="${HOME}/.pyenv"
    export PATH="${PYENV_ROOT}/bin:${PATH}"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
fi

if which rbenv > /dev/null; then
    eval "$(rbenv init -)"
fi

if which nodenv > /dev/null; then
    export PATH="${HOME}/.nodenv/bin:${PATH}"
    eval "$(nodenv init -)"
fi

PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
PATH="${PATH}:${HOME}/bin"

# EDITOR
# CVS_EDITOR
# GIT_EDITOR
# SVN_EDITOR
export EDITOR="emacsclient -c -t"
export CVS_EDITOR="emacsclient -c -t"
export GIT_EDITOR="emacsclient -c -t"
export SVN_EDITOR="emacsclient -c -t"

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="UTF-8"
export LANG="en_US.UTF-8"

# Configure Golang environment
export GOPATH="${HOME}/Projects"
