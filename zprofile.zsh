# echo "zprofile.zsh"

if [[ "${OSTYPE}" =~ "darwin"* ]]; then
    # Add Homebrew patch (/opt/homebrew/bin) to PATH
    eval "$(/opt/homebrew/bin/brew shellenv)"

    # For some reason, my MacBook Pro 14" does not do tab-completion for
    # Homebrew so this allows the tab-completion to work.
    if type brew > /dev/null 2>&1; then
        FPATH=$(brew --prefix)/completions/zsh:${FPATH}
        autoload -Uz compinit
        compinit
    fi

    # Building Python via pyenv install...
    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix bzip2)/include"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix bzip2)/lib"
    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix zlib)/include"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix zlib)/lib"

    if which pyenv > /dev/null; then
        export PYENV_ROOT="${HOME}/.pyenv"
        export PATH="${PYENV_ROOT}/bin:${PATH}"
        eval "$(pyenv init -)"
    fi

    if which rbenv > /dev/null; then
        eval "$(rbenv init -)"
    fi

    if which nodenv > /dev/null; then
        eval "$(nodenv init -)"
    fi

    # MacTex (brew install --cask mactex) is a Universal binary package
    PATH="${PATH}:/usr/local/texlive/2023/bin/universal-darwin"

elif [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
    PATH="/usr/local/bin:/usr/local/sbin"
    PATH="${PATH}:/usr/games"
    PATH="${PATH}:/usr/bin:/bin"
    PATH="${PATH}:/usr/sbin:/sbin"

    # Configure LD_LIBRARY_PATH for Pop!_OS
    export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"

    if [[ -x "${HOME}/.pyenv/bin/pyenv" ]]; then
        export PYENV_ROOT="${HOME}/.pyenv"
        export PATH="${PYENV_ROOT}/bin:${PATH}"
        eval "$(pyenv init --path)"
        eval "$(pyenv init -)"
    fi

    # rbenv looks a bit old under Pop!_OS
    # PATH="${PATH}:${HOME}/.gem/ruby/2.5.0/bin"

    if [[ -x "${HOME}/.rbenv/bin/rbenv" ]]; then
        export RBENV_ROOT="${HOME}/.rbenv"
        export PATH="${RBENV_ROOT}/bin:${PATH}"
        eval "$(rbenv init - zsh)"
    fi

    if [[ -x "${HOME}/.nodenv/bin/nodenv" ]]; then
        export NODENV_ROOT="${HOME}/.nodenv"
        export PATH="${NODENV_ROOT}/bin:${PATH}"
        eval "$(nodenv init -)"
    fi
fi

PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
PATH="${PATH}:${HOME}/bin"
