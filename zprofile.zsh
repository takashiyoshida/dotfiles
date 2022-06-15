# echo "zprofile.zsh"

if [[ "${OSTYPE}" =~ darwin* ]]; then
    # This is taken care of in zshenv.sh
    # echo "HOMEBREW_PREFIX=${HOMEBREW_PREFIX}"
    # Display an interesting login message
    ${HOMEBREW_PREFIX}/bin/fortune | ${HOMEBREW_PREFIX}/bin/cowsay | ${HOMEBREW_PREFIX}/bin/lolcat
fi
