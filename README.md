# dotfiles

```
There are many like it but this one is mine.
```

## Installation

My dotfiles use assumes that your default shell is `zsh`.


``` bash
cd ${HOME}/Projects
git clone --recurse-submodules https://github.com/takashiyoshida/dotfiles.git
```


## Dependencies

### Homebrew

``` bash
brew install peco
brew install knqyf263/pet/pet
```

- [peco/peco: Simplistic interactive filtering tool](https://github.com/peco/peco)
- [knqyf263/pet: Simple command-line snippet manager, written in Go](https://github.com/knqyf263/pet)

- List of all installed Homebrew formulae

### GitHub Repositories

- [peco/peco: Simplistic interactive filtering tool](https://github.com/peco/peco)
- [knqyf263/pet: Simple command-line snippet manager, written in Go](https://github.com/knqyf263/pet)
- [tomislav/osx-terminal.app-colors-solarized: Solarized color theme for OS X 10.7+ Terminal.app](https://github.com/tomislav/osx-terminal.app-colors-solarized)
- [timsutton/osx-vm-templates: macOS templates for Packer and VeeWee](https://github.com/timsutton/osx-vm-templates)

## Keybindings

### Zsh

- `Ctrl-]`: Use `ghq --list` and `peco` to go to one of the locally installed repositories.
- `Ctrl-R`: Search command history using `peco`
- `Ctrl-S`: Use `pet` to search for snippet

### Hammerspoon

- `Cmd-Ctrl-U`: Move the top most window to the top left corner of the desktop
- `Cmd-Ctrl-O`: Move the top most window to the top right corner of the desktop
- `Cmd-Ctrl-J`: Move the top most window to the bottom left corner of the desktop
- `Cmd-Ctrl-L`: Move the top most window to the bottom right coner of the desktop

- `Cmd-Option-Ctrl-C`: Move the current window to the center of the desktop
- `Cmd-Option-Ctrl-V`: Extend the current window size vertically to the bottom of the desktop
