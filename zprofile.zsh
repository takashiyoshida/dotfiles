# .zprofile is similar to .zlogin, except that it is sourced before .zshrc.
# .zprofile is meant as an alternative to .zlogin for ksh fans; the two are
# not intended to be used together, although this could certainly be done if desired.
# Reference: https://zsh.sourceforge.io/Intro/intro_3.html

if [[ "${OSTYPE}" =~ "darwin"* ]]; then
	# Add Homebrew to macOS environment (this was added when I installed Homebrew)
	eval "$(/opt/homebrew/bin/brew shellenv)"
	
	# Add tab-completion to Homebrew command
	if type brew &> /dev/null; then
		FPATH="$(brew --prefix)/share/zsh/site-functions:${FPATH}"
		autoload -Uz compinit
		compinit
	fi

	# Set up pyenv for shell environment
	if which pyenv > /dev/null; then
		export PYENV_ROOT="${HOME}/.pyenv"
		export PATH="${PYENV_ROOT}/bin:${PATH}"
		eval "$(pyenv init -)"
	fi
	
	# Set up rbenv for shell environment
	if which rbenv > /dev/null; then
		eval "$(rbenv init -)"
	fi
	
	# Set up nodenv for shell environment
	if which nodenv > /dev/null; then
		eval "$(nodenv init -)"
	fi

	# Add MacTex to PATH (MacTex is a Universal binary package)
	# I am mostly interested in pdflatex to convert Markdown file to PDF.
	# I found out in macOS Sonoma that pdflatex already exists at
	# /Library/TeX/texbin/pdflatex.
	# PATH="${PATH}:/usr/local/texlive/2023/bin/universal-darwin"

elif [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
	PATH="/usr/local/bin:/usr/local/sbin"
	PATH="${PATH}:/usr/games"
	PATH="${PATH}:/usr/bin:/bin"
	PATH="${PATH}:/usr/sbin:/sbin"
	
	# Set up pyenv for shell environment
	if [[ -x "${HOME}/.pyenv/bin/pyenv" ]]; then
		export PYENV_ROOT="${HOME}/.pyenv"
		export PATH="${PYENV_ROOT}/bin:${PATH}"
		eval "$(pyenv init --path)"
		eval "$(pyenv init -)"
	fi
	
	# Set up rbenv for shell environment
	if [[ -x "${HOME}/.rbenv/bin/rbenv" ]]; then
		export RBENV_ROOT="${HOME}/.rbenv"
		export PATH="${RBENV_ROOT}/bin:${PATH}"
		eval "$(rbenv init -zsh)"
	fi
	
	if [[ -x "${HOME}/.nodenv/bin/nodenv" ]]; then
		export NODENV_ROOT="${HOME}/.nodenv"
		export PATH="${NODENV_ROOT}/bin:${PATH}"
		eval "$(nodenv init -)"
	fi
fi

PATH="${PATH}:${HOME}/Projects/dotfiles/bin"
PATH="${PATH}:${HOME}/bin"

export TERM=xterm-256color
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="UTF-8"
export LANG="en_US.UTF-8"

export EDITOR="emacsclient -c -t"
export CVS_EDITOR="${EDITOR}"
export SVN_EDITOR="${EDITOR}"
export GIT_EDITOR="${EDITOR}"

export GOPATH="${HOME}/Projects"
