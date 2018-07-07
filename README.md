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

- `Ctrl-]`: Use `ghq --list` and `peco` to go to one of the locally installed repositories.
- `Ctrl-R`: Search command history using `peco`
- `Ctrl-S`: Use `pet` to search for snippet
