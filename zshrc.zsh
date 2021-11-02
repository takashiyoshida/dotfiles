if [[ "${OSTYPE}" =~ linux-gnu* ]]; then
    # Source .zprofile
    case $- in
        *i*) # interactive shell
            source ${HOME}/.zprofile
            ;;
        *) # non-interactive shell
            # Should already have sourced .zprofile
            ;;
    esac
fi

# Path to your oh-my-zsh configuration.
ZSH="${HOME}/Projects/dotfiles/zsh"

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="takashiyoshida"

# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Uncomment this to disable bi-weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment to change how often before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want to disable command autocorrection
# DISABLE_CORRECTION="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

# Uncomment following line if you want to disable marking untracked files under
# VCS as dirty. This makes repository status check for large repositories much,
# much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
if [[ "${OSTYPE}" =~ darwin* ]]; then
    plugins=(colored-man-pages docker extract gem golang osx python rake ruby ssh-agent svn tmux vagrant)
else
    plugins=(colored-man-pages debian docker extract gem golang python rake ruby ssh-agent svn tmux vagrant)
fi

source $ZSH/oh-my-zsh.sh

# Customize to your needs...

# Minimum set of aliases
alias mv="mv -i"
alias cp="cp -i"
alias rm="rm -i"

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

alias rake="noglob rake"

export DOTFILES="${HOME}/Projects/dotfiles/scripts"
source "${DOTFILES}/aliases.zsh"
source "${DOTFILES}/peco.zsh"
source "${HOME}/.projects.zsh"
source "${HOME}/.secrets.zsh"

# Add SSH keys
add-ssh-private-keys

# Start emacs service (macOS)
start-emacs-service
