'''
See: https://github.com/vim-scripts/DrawIt
'''

from typing import Tuple, List

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

    @neovim.command('BoxSelected')
    def box_selected(self) -> None:
        lpos = Position(self.vim.eval('getpos("\'<")'))
        lpos.column = min(len(self.vim.current.buffer[lpos.line - 1]),
                          lpos.column)
        rpos = Position(self.vim.eval('getpos("\'>")'))
        rpos.column = min(len(self.vim.current.buffer[rpos.line - 1]),
                          rpos.column)
        box_area(self.vim.current.buffer,
                 Coords(lpos.column - 1, lpos.line - 1),
                 Coords(rpos.column - 1, rpos.line - 1))


class Position:
    """Wraps vim function getpos() result and makes it more readable.

    Vim docs:
        getpos({expr})

        The result is a |List| with four numbers:
            [bufnum, lnum, col, off]
        "bufnum" is zero, unless a mark like '0 or 'A is used, then it
        is the buffer number of the mark.
        "lnum" and "col" are the position in the buffer.  The first
        column is 1.
        The "off" number is zero, unless 'virtualedit' is used.  Then
        it is the offset in screen columns from the start of the
        character.  E.g., a position within a <Tab> or after the last
        character.
    """

    def __init__(self, params: List[int]) -> None:
        self.buff = params[0]
        self.line = params[1]
        self.column = params[2]
        self.off = params[3]


class Coords:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def box_area(lines: neovim.api.Buffer, top_left: Coords,
             bottom_right: Coords) -> List[str]:
    for y in range(top_left.y, bottom_right.y + 1):
        lines[y] = with_vertical_borders(lines[y], top_left.x, bottom_right.x)
    ln_border = horizontal_border(top_left.x, bottom_right.x)
    lines.append(ln_border, top_left.y)
    lines.append(ln_border, bottom_right.y + 2)
    return lines


def with_vertical_borders(line: str, x1: str, x2: str) -> str:
    prefix = line[:x1]
    suffix = line[x2 + 1:]
    selected = line[x1:x2 + 1]
    return '{}| {} |{}'.format(prefix, selected, suffix)


def horizontal_border(x1: int, x2: int) -> str:
    padding = ' ' * x1
    border = '-' * (x2 - x1 + 3)
    return '{}+{}+'.format(padding, border)


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
    lpos = Position([0, 1, 1, 0])
    rpos = Position([0, 2, 10, 0])
    box_area(vim.current.buffer,
             Coords(lpos.column - 1, lpos.line - 1),
             Coords(rpos.column - 1, rpos.line - 1))
