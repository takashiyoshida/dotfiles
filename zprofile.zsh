# Configure Golang environment
export GOPATH="${HOME}/Projects"

# Configure PATH variable
# Default PATH (macOS Big Sur)
# PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin
# - /usr/local/bin
# - /usr/bin
# - /bin
# - /usr/sbin
# - /sbin
# - /Library/Apple/usr/bin

# MacTex (brew install --cask mactex) is a Universal binary package
# Installed by mactex-20210328.pkg release works with macOS Big Sur (including Apple Silicon)
if [[ "${OSTYPE}" =~ darwin* ]]; then
    PATH="${PATH}:/usr/local/texlive/2021/bin/universal-darwin"
fi

PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
PATH="${PATH}:${HOME}/bin"

# Add Homebrew path (/opt/homebrew/bin) to PATH
eval "$(/opt/homebrew/bin/brew shellenv)"

# Configure LD_LIBRARY_PATH
if [[ "${OSTYPE}" =~ linux-gnu* ]]; then
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"
    export LD_LIBRARY_PATH
fi

# Configure Python, Ruby and Node.js
# Python
if which pyenv > /dev/null; then
	export PYENV_ROOT="${HOME}/.pyenv"
	export PATH="${PYENV_ROOT}/bin:${PATH}"
    eval "$(pyenv init --path)"

    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix bzip2)/include"
    CPPFLAGS="${CPPFLAGS} -I$(brew --prefix zlib)/include"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix bzip2)/lib"
    LDFLAGS="${LDFLAGS} -L$(brew --prefix bzip2)/lib"

    export CPPFLAGS
    export LDFLAGS
fi

# Ruby
if [[ "${OSTYPE}" =~ darwin* ]]; then
    if which rbenv > /dev/null; then
        eval "$(rbenv init -)"
    fi
else
    # rbenv looks a bit old for Pop!_OS
    PATH="${PATH}:${HOME}/.gem/ruby/2.5.0/bin"
fi

# Node.js
if which nodenv > /dev/null; then
    export PATH="${HOME}/.nodenv/bin:${PATH}"
    eval "$(nodenv init -)"
fi

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="UTF-8"
export LANG="en_US.UTF-8"

# EDITOR
# CVS_EDITOR
# GIT_EDITOR
# SVN_EDITOR
export EDITOR="emacsclient -c -t"
export CVS_EDITOR="emacsclient -c -t"
export GIT_EDITOR="emacsclient -c -t"
export SVN_EDITOR="emacsclient -c -t"
