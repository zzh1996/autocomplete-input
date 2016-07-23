#!/usr/bin/env python3
# encoding: utf-8

from curses import *
from autocomplete import *


def render_choice(stdscr, c, selected):
    highlight = A_STANDOUT if selected else 0
    while c:
        p = c.find('<b>')
        q = c.find('</b>')
        if p >= 0 and p < q:
            stdscr.addstr(c[:p], highlight)
            stdscr.addstr(c[p + 3:q], A_BOLD | highlight)
            c = c[q + 4:]
        else:
            stdscr.addstr(c, highlight)
            break


def main(stdscr):
    stdscr.clear()
    text = ''
    pos = 0
    choice = 0
    choice_cnt = 0
    change = False
    choices = []
    while True:
        k = stdscr.getch()
        change = False
        if k == KEY_DOWN:
            if choice < choice_cnt - 1:
                choice += 1
        elif k == KEY_UP:
            if choice > 0:
                choice -= 1
        elif k == KEY_LEFT:
            if pos > 0:
                pos -= 1
        elif k == KEY_RIGHT:
            if pos < len(text):
                pos += 1
        elif k == ord('\t'):
            if choice_cnt > 0:
                text = choices[choice].replace('<b>','').replace('</b>','')
                pos=len(text)
                change = True
        elif k == ord('\n'):
            return
        elif k == KEY_BACKSPACE:
            if pos > 0:
                text = text[:pos - 1] + text[pos:]
                pos -= 1
                change = True
        else:
            text = text[:pos] + chr(k) + text[pos:]
            pos += 1
            change = True

        stdscr.clear()
        stdscr.addstr(0, 0, text)
        stdscr.move(0, pos)
        stdscr.refresh()
        if change:
            choices = google(text, pos)
            choice = 0
            choice_cnt = len(choices)
        for i, c in enumerate(choices):
            stdscr.move(i + 1, 0)
            render_choice(stdscr, c, i == choice)
        stdscr.move(0, pos)
        stdscr.refresh()


wrapper(main)
