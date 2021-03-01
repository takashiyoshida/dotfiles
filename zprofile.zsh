# Configure Golang environment
export GOPATH="${HOME}/Projects"

# Configure PATH variable
PATH="/usr/local/bin:/usr/local/sbin"
PATH="${PATH}:/usr/bin:/usr/sbin"
PATH="${PATH}:/bin:/sbin"

# Not sure about /usr/local/go/bin in non-macOS environment
PATH="${PATH}:/usr/local/go/bin"
PATH="${PATH}:${GOPATH}/bin"

if [[ "${OSTYPE}" =~ darwin* ]]; then
    # Installed by MacTex; 2019.0508 release works with macOS Catalina
    PATH="${PATH}:/usr/local/texlive/2020/bin/x86_64-darwin"
fi

PATH="${PATH}:${HOME}/bin"
PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
export PATH

# Configure LD_LIBRARY_PATH
if [[ "${OSTYPE}" =~ linux-gnu* ]]; then
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"
    export LD_LIBRARY_PATH
fi

# Configure Python, Ruby and Node.js
# Python
if which pyenv > /dev/null; then
    eval "$(pyenv init -)"

    # It is better to use `brew --prefix` so that I do not need to hardcode the path
    # to zlib and bzip2. But `brew --prefix` runs a bit slow and causes the zsh startup
    # time to be longer.
	# export LDFLAGS="-L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib"
	# export CPPFLAGS="-I$(brew --prefix zlib)/include -I$(brew --prefix bzip2)/include"
	export LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/bzip2/lib"
	export CPPFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/bzip2/include"
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

# Homebrew access token
# TODO: Assign your own access token
export HOMEBREW_GITHUB_API_TOKEN=""

# EDITOR
# CVS_EDITOR
# GIT_EDITOR
# SVN_EDITOR
export EDITOR="emacsclient -c -t"
export CVS_EDITOR="emacsclient -c -t"
export GIT_EDITOR="emacsclient -c -t"
export SVN_EDITOR="emacsclient -c -t"

