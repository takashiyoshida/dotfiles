# dotfiles

```
There are many like it but this one is mine.
```

## Dependencies

- Homebrew
- zsh
- nodenv
- pyenv
- rbenv
- tmux
- Hammerspoon

### Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

### zsh

```bash
brew install zsh
sudo echo "/usr/local/bin/zsh" >> /etc/shells
chsh -s /usr/local/bin/zsh
```

### Emacs

```bash
brew tap d12frosted/emacs-plus
brew install emacs-plus
```

### nodenv, pyenv, rbenv

```bash
brew install nodenv
brew install pyenv
brew install rbenv
```

### peco

```bash
brew install peco
```

### tmux

```bash
brew install tmux
```

### Hammerspoon

Download and install the latest release from [Hammerspoon](https://www.hammerspoon.org).

## Installation

```bash
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
