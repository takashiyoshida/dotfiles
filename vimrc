" Copied from [Toolkit] Configuring Your Vim https://medium.com/the-new-blackboard/toolkit-configuring-your-vim-42eb09bcb55f

" This option makes Vim behave in a more useful way.
set nocompatible
" There are potential security implications to having modelines on (though they
" are cool).  If you don't know what they are, it's better not to mess with it.
set nomodeline

" This is turning on three related options for filetypes; detection, plugins,
" and indentation.  Vim will autodetect a lot of filetypes and turn on custom
" options/indentation rules per filetype.
filetype plugin indent on

" Turns on syntax highlighting.  If you want to use a custom color scheme, it
" should be loaded *after* turning on syntax.
syntax on

" Enables the mouse in all modes.  This means copying will require holding
" shift.
set mouse=a

" Turns on the wildmenu.  When on, command-line (the mode when you start with a
" `:`) completion operates in an "enhanced" mode.
set wildmode=longest:full,full
set wildmenu

" Sets the maximum width of text that is being inserted.
set textwidth=80
" The sequence of letters describes how automatic formatting is to be done.
" c - Auto-wrap comments using textwidth, inserting the current comment leader
"     automatically
" q - Allow formatting of comments with "gq".
set formatoptions=cq

" Turns on line numbers.
set number

" Sets the minimum number of screen lines to keep above and below the cursor.
set scrolloff=5

" Sets backspace to work the way you'd expect it to.
set backspace=indent,eol,start
" Allow arrow keys to work the way you'd expect them to.
set whichwrap+=<,>

" Copy indent from current line when starting a new line.
set autoindent

" Sets indentation settings
" softtabstop sets how many spaces pressing tab/bs will insert/delete
" shiftwidth sets how many spaces are used for each indentation level
" expandtab makes vim insert spaces instead of tab characters
" shiftround rounds the indentation to a multiple of shiftwidth
" Some filetype plugins (remember those things we turned on earlier) will
" override these.  For example, python's probably sets default indentation to 4
" spaces.
set softtabstop=3 shiftwidth=3 expandtab shiftround

" Turns on incremental search
set incsearch

" Show the line and column number of the cursor position in the lower right.
set ruler
" Show partial commands in the last line of the screen.
set showcmd
