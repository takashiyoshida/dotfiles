# .zshenv is sourced on all invocations of the shell, unless -f option is set.
# It should contain commands to set the command search path, plus other
# important environment variables.
# 
# .zshenv should not contain commands that produce output or assume the shell
# is attached to a tty.
# Reference: # echo "$(date) Sourcing .zlogin ..."

# 2023-11-24: I moved this from .zprofile to .zshenv but this somehow caused
#             `brew doctor` command to report /usr/bin occurs before
#             /opt/homebrew/bin in my PATH variable.
# Don't run this in .zshenv file
# eval "$(/opt/homebrew/bin/brew shellenv)"
