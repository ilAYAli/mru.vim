# MRU

MRU, most recently used files, possibly colorized and with devicons.
Per _git repo_ database. Per _user_ database for all other files.

### Installation
    pip3 install -r requirements.txt

* https://github.com/junegunn/fzf.vim (for vim integration)
* https://github.com/ryanoasis/nerd-fonts (only if `mru_use_devicons` is enabled)


### Vim-Plug

    Plug 'ilayali/mru.vim'

### Configuration
Default parameters can be specified in the following manner:
* `~/.mru.conf` (see `config/.mru.conf` for an example)
* neo/vim specific parameters:

    Enable devicons:

      let g:mru_use_devicons = 1

    Enable colors:

      let g:mru_use_colors == 1

### Neo/Vim options
    MRU                             print MRU
    MRU --add /path/to/file         delete entry from MRU
    MRU --del /path/to/file         add entry to MRU


### CML options
    usage: mru [-h] [-a] [-d] [-m] [-v] [-c] [-i]

    optional arguments:
      -h, --help      show this help message and exit
      -a , --add      add file to MRU
      -d , --delete   delete file from MRU
      -m , --max      max MRU size
      -v, --verbose   verbose
      -c, --colors    print with colors
      -i, --icons     show icons (requires NERD fonts)


To pipe the output to fzf: `mru -i -c | fzf --ansi`  
To pipe the output to less: `mru -i -c | less -REX`


![screenshot](http://github.com/ilAYAli/mru.vim/edit/master/img/ss-vim.png)
