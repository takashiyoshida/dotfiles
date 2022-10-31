# echo "zshrc.zsh"

# Uncomment the following line to debug zsh startup time
# Reference: https://gist.github.com/elalemanyo/cb3395af64ac23df2e0c3ded8bd63b2f
#
# zmodload zsh/zprof

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

if [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
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
export DOTFILES="${HOME}/Projects/dotfiles"
ZSH="${DOTFILES}/zsh"

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
source "${DOTFILES}/powerlevel10k/powerlevel10k.zsh-theme"
[[ ! -f "${HOME}/.p10k.zsh" ]] || source ${HOME}/.p10k.zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
# Disabled because I'm using powerlevel10k to configure ZSH theme
# ZSH_THEME="takashiyoshida"

# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# Minimum set of aliases
alias mv="mv -i"
alias cp="cp -i"
alias rm="rm -i"

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

alias rake="noglob rake"

# The rest of aliases are defined further down below...

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
if [[ "${OSTYPE}" =~ "darwin"* ]]; then
    plugins=(autojump colored-man-pages docker fzf gem golang macos pyenv python rake rbenv ruby tmux)
elif [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
    plugins=(colored-man-pages docker gem golang pyenv python rake rbenv ruby ssh-agent svn tmux vagrant)
fi

source $ZSH/oh-my-zsh.sh

# Customize to your needs...
# Load the rest of generic aliases and platform-specific aliases
source "${DOTFILES}/scripts/aliases.zsh"
# This should be called only after sourcing the ${DOTFILES}/aliases.zsh file
if [[ "${OSTYPE}" =~ darwin* ]]; then
    if [ -f /opt/homebrew/etc/profile.d/autojump.sh ]; then
        source /opt/homebrew/etc/profile.d/autojump.sh
    fi

    if [ -e "${HOME}/.iterm2_shell_integration.zsh" ]; then
        source "${HOME}/.iterm2_shell_integration.zsh"
    fi

    add-ssh-private-keys
fi

# eval "$(${RBENV_ROOT}/bin/rbenv init - zsh)"

source "${HOME}/.projects.zsh"
source "${HOME}/.secrets.zsh"

# Uncomment the following line to enable zsh startup time
# zprof
# Finally, run `time zsh -i -c exit`

