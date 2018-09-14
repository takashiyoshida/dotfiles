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

export DOTFILES="${HOME}/Projects/dotfiles/scripts"
# PATH, EDITOR, CVSEDITOR, GITEDITOR, SVNEDITOR
source "${DOTFILES}/variables.zsh"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
if [[ "${OSTYPE}" =~ darwin* ]]; then
    # for macOS
    plugins=(colored-man docker gem go hub osx python rake ruby svn tmux vagrant)
else
    # and everything else here, but mainly Linux
    plugins=(colored-man docker gem go hub python rake ruby svn tmux vagrant)
fi

source $ZSH/oh-my-zsh.sh

# Customize to your needs...

# Minimum set of aliases
alias ls="ls --color=auto -CFG"
alias mv="mv -i"
alias cp="cp -i"
alias rm="rm -i"

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

alias rake="noglob rake"

source "${DOTFILES}/aliases.zsh"
source "${DOTFILES}/peco.zsh"
source "${DOTFILES}/pet.zsh"
