# Set the TERM to xterm-24bit so that Emacs looks nicer in terminal
# But do this for macOS only
if [[ "${OSTYPE}" =~ darwin* ]]; then
    export TERM=xterm-24bit
fi
