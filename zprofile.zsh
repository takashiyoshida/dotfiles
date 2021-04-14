# Configure Golang environment
export GOPATH="${HOME}/Projects"

# Configure PATH variable

# Default PATH
# PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin
# - /usr/local/bin
# - /usr/bin
# - /bin
# - /usr/sbin
# - /sbin
# - /Library/Apple/usr/bin

# Not sure about /usr/local/go/bin in non-macOS environment
#PATH="${PATH}:/usr/local/go/bin"
#PATH="${PATH}:${GOPATH}/bin"

# Disable this for now, as MacTex is not ready for Apple Silicon
# if [[ "${OSTYPE}" =~ darwin* ]]; then
    # Installed by MacTex; 2019.0508 release works with macOS Catalina
    # PATH="${PATH}:/usr/local/texlive/2020/bin/x86_64-darwin"
# fi

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
    eval "$(pyenv init -)"

	export LDFLAGS="-L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib"
	export CPPFLAGS="-I$(brew --prefix zlib)/include -I$(brew --prefix bzip2)/include"
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
