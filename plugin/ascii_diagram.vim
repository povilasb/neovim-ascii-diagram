if exists ('g:loaded_ascii_diagram') || !has('nvim') || !has('python3')
    finish
endif
let g:loaded_ascii_diagram = 1

nnoremap <c-b> :BoxWord<CR>
