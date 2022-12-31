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

- `left_control` key posts `escape` when it is pressed alone. This is useful in canceling a dialog or in `Vim`.
- `left_control` key posts `left_control` when it is held down with other keys. This is useful in `Emacs` and macOS Emacs key bindings.

### Craft

- `Left Control` + `p` posts `up_arrow`
- `Left Control` + `n` posts `down_arrow`
- `Left Control` + `d` posts `delete_forward`

### Microsoft Office

- Add Emacs-like key bindings to Microsoft Office
    - `Control` + `fbnpae` for cursor movement
