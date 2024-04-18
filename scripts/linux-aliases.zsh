alias ls="ls -CF --color=auto"
alias lh="ls -lh"
alias lah="ls -lah"
alias lll="ll | less"
alias llr="ll -R"

alias svndiff="svn diff --diff-cmd /usr/bin/diff -x -w"
alias svnldiff="svndiff -r COMMITTED" # Show the last commit
alias svninfo="svn info --show-item=url"
# Ignore unversioned files from svn status
alias svnst="svn status -q"
alias svnstc="svnst | ag \"^C\""

alias vless="/usr/share/vim/vim82/macros/less.sh"
alias apti="apt list --installed 2> /dev/null"

# Copy the Github API token from a hidden file
alias ghtoken="xclip -sel clip < ${HOME}/.github-tokens.txt"

# Simulate macOS' `open' command
alias open="xdg-open"

# Copied from https://www.youtube.com/shorts/K1FxGIG_lcA
alias nv="fdfind --type f --hidden --exclude .git | fzf-tmux -p --reverse | xargs nvim"
