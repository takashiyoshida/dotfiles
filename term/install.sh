#!/usr/bin/env zsh

echo "Installing xterm-24bit.terminfo ..."
/usr/bin/tic -x -o ${HOME}/.terminfo xterm-24bit.terminfo

echo "Done"
