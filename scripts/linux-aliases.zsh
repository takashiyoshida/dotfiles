if [[ "${OSTYPE}" =~ "linux-gnu"* ]]; then
    alias ls="ls -CF --color=auto"
    alias apti="apt list --installed 2> /dev/null"

    alias vless="/usr/share/vim/vim82/macros/less.sh"

    # Copy the Github API token from a hidden file
    alias ghtoken="xclip -sel clip < ${HOME}/.github-tokens.txt"

    # Simulate macOS' `open' command
    alias open="xdg-open"
fi
