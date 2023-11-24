# .zlogin is sourced in login shells. It should contain commands that should
# be executed only in login shells.
# Reference: https://zsh.sourceforge.io/Intro/intro_3.html

if [[ "${OSTYPE}" =~ "darwin"* ]]; then
	# Unfortunately, powerlevel10k triggers a warning message when startup files
	# emit output.
	# fortune | cowsay | loclcat --force
elif [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
	# /usr/games/fortune | /usr/games/cowsay | lolcat --force
fi
