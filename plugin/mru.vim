if exists('g:mru_loaded')
    finish
endif
let g:mru_loaded = 1

if ! executable('python3')
    throw "error, python3 not found"
endif

" configuration:
let g:mru_use_devicons = get(g:, 'mru_use_devicons', 1)
let g:mru_use_colors = get(g:, 'mru_use_colors', 1)

" argument(s) to mru script
let g:mru_bin_args = ""
let g:mru_bin_args = g:mru_bin_args . " --icons"
let g:mru_bin_args = g:mru_bin_args . " --colors"
let g:mru_bin_args = g:mru_bin_args . " --max 1000"

let g:mru_bin_args = " --colors --icons --max 1000"
let s:mru_bin = expand('<sfile>:p:h') . '/../python/mru.py'

function! s:Add()
    silent! execute "!" . s:mru_bin . ' --add %:p'
endfunction

augroup mru_autocmd
    autocmd!
    autocmd BufEnter * call s:Add()
augroup END

function! s:edit_devicon_prepended_file(item)
    let l:file_path = split(a:item, ':')[1]
    silent! execute 'silent! e' l:file_path
endfunction

function! s:MRU(...)
    let l:fn = expand('%')
    if len(l:fn)
        let g:mru_bin_args = g:mru_bin_args . ' --exclude ' . expand('%')
    endif
    if a:0 == 0
        let l:fzf_files_options = '--ansi'
        call fzf#run({
          \ 'source': s:mru_bin . g:mru_bin_args,
          \ 'sink':   function('s:edit_devicon_prepended_file'),
          \ 'options': '-m ' . l:fzf_files_options,
          \ 'down':    '30%' })
    else
        silent! execute "!" . s:mru_bin . " " . join(a:000)
    endif
endfunction

command! -nargs=? MRU call s:MRU(<f-args>)
