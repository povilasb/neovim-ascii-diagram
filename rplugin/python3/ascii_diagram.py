'''
See: https://github.com/vim-scripts/DrawIt
'''

from typing import Tuple

import neovim


@neovim.plugin
class AsciiDiagram(object):
    def __init__(self, vim) -> None:
        self.vim = vim

    @neovim.command('BoxWord', eval='expand("<cword>")')
    def box_word(self, word: str) -> None:
        curr_col = self.vim.eval('col(".")')
        line_bellow, new_line = box_word(self.vim.current.line, curr_col)
        self.vim.current.line = new_line

        buff = self.vim.current.buffer
        curr_ln = self.vim.eval('line(".")') - 1
        buff.append(line_bellow, curr_ln)
        buff.append(line_bellow, curr_ln + 2)


def word_starts(line: str, char_pos: int) -> int:
    while char_pos > 0 and line[char_pos] != ' ':
        char_pos -= 1
    if line[char_pos] == ' ':
        char_pos += 1
    return char_pos


def word_ends(line: str, char_pos: int) -> int:
    while char_pos < len(line) - 1 and line[char_pos] != ' ':
        char_pos += 1
    if line[char_pos] == ' ':
        char_pos -= 1
    return char_pos


def word_bounds(line: str, char_pos: int) -> Tuple[int, int]:
    return (word_starts(line, char_pos), word_ends(line, char_pos))


def box_word(ln: str, char_pos: int) -> Tuple[str, str]:
    start, end = word_bounds(ln, char_pos)
    prefix = ln[:start]
    suffix = ln[end + 1:]
    selected_word = ln[start:end + 1]
    ln_bellow = '{}+-{}-+{}'.format(
        ' ' * len(prefix),
        '-' * len(selected_word),
        ' ' * len(prefix),
    )
    new_ln = '{}| {} |{}'.format(prefix, selected_word, suffix)
    return ln_bellow, new_ln


def test() -> None:
    vim = neovim.attach('socket', path='/tmp/nvim')
    curr_col = vim.eval('col(".")')
    line_bellow, new_line = box_word(vim.current.line, curr_col)
    vim.current.line = new_line
    buff = vim.current.buffer
    curr_ln = vim.eval('line(".")') - 1
    buff.append(line_bellow, curr_ln)
    buff.append(line_bellow, curr_ln + 2)