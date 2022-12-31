# README

## Simple Modifications

### Built-in Keyboard

#### Caps Lock

- `caps_lock` key is mapped to `left_control` key

### All Devices

#### Escape

- `escape` key is mapped to `apple_vendor_keyboard_key_code function` key

## Complex Modifications

### Left Control

- `left_control` key posts `escape` when it is pressed alone. This is useful in canceling a dialog or in Vim.

- `left_control` key posts `left_control` when it is held down with other keys. This is useful in `Emacs` and macOS Emacs key bindings.

### Right Command

- Tap `right_command` twice to send `command` + `option` + `control`

- Tab `right_command` once to send `right_command`s

### Craft

- `left_control` + `p` posts `up_arrow`
- `left_control` + `n` posts `down_arrow`

### Microsoft Office

- Add Emacs-like key bindings to move cursor in Microsoft Office applications

- `left_control` + `f` posts `right_arrow`
- `left_control` + `b` posts `left_arrow`
- `left_control` + `n` posts `down_arrow`
- `left_control` + `p` posts `up_arrow`
- `left_control` + `a` posts `home`
- `left_control` + `e` posts `end`
