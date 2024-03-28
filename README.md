# dotfiles

```
There are many like it but this one is mine.
```

## Dependencies

### macOS Pre-Requisites

#### Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Below shows some of software packages I use. But it would be far easier to install all packages by running `brew bundle install` instead.

#### Install Zsh

```bash
brew install zsh
sudo echo "/usr/local/bin/zsh" >> /etc/shells
chsh -s /usr/local/bin/zsh
```

#### Install Emacs

```bash
brew tap d12frosted/emacs-plus
brew install emacs-plus
```

#### Install nodenv, pyenv, rbenv

```bash
brew install nodenv
brew install pyenv
brew install rbenv
```

#### Install peco

```bash
brew install peco
```

> I no longer use peco. I use [fzf](https://github.com/junegunn/fzf) instead.

#### Install tmux

```bash
brew install tmux
```

#### Install Hammerspoon

Download and install the latest release from [Hammerspoon](https://www.hammerspoon.org).

---
### Linux Pre-Requisites

## Linux (Pop!_OS)

1. Copy `emacs.service` to `~/.config/systemd/user/`.

```bash
mkdir -p ~/.config/systemd/user/
cp emacs.service ~/.config/systemd/user/
```

2. Run `systemctl --user enable emacs.service`.
3. Run `systemctl --user start emacs.service`.

- Refer to instructions at [Emacs As Daemon](https://www.emacswiki.org/emacs/EmacsAsDaemon)

---

## Installation

```bash
mkdir ${HOME}/Projects
git clone https://github.com/takashiyoshida/dotfiles.git ~/Projects/dotfiles
cd Projects/dotfiles
rake
```

## References

- Homebrew
- [peco/peco: Simplistic interactive filtering tool](https://github.com/peco/peco)



### GitHub Repositories

- [tomislav/osx-terminal.app-colors-solarized: Solarized color theme for OS X 10.7+ Terminal.app](https://github.com/tomislav/osx-terminal.app-colors-solarized)
- [timsutton/osx-vm-templates: macOS templates for Packer and VeeWee](https://github.com/timsutton/osx-vm-templates)

- [syl20bnr/spacemacs - Terminal](https://github.com/syl20bnr/spacemacs/wiki/Terminal)
