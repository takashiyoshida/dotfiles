# echo "zshenv.zsh"

# For macOS, do not configure PATH here as /etc/zprofile will call
# `/usr/libexec/path_helper -s` to configure PATH variable.
# In Linux, /etc/zsh/zprofile file is empty and does not set PATH variable.

export TERM=xterm-256color

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
