=====
About
=====

This is a wannabe remote Neovim plugin that helps to draw ASCII diagrams::

    +--------+  GET    +--------+
    | Client | ------> | Server |
    +--------+         +--------+
      ^                   |
      |     200 OK        |
      +-------------------+

It requires Python > 3.4.

Something like https://github.com/vim-scripts/DrawIt, but implemented in
Python. Thus more extensible and maintainable.

Installation
============

1. Put `plugin/` and `rplugin/` to `~/.config/nvim`;
2. Open neovim and in command mode type `:UpdateRemotePlugins`

Usage
=====

Move cursor onto the word and press `CTRL+b`.

.. image:: usage.gif
