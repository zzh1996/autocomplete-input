#!/usr/bin/env python3
# encoding: utf-8

from curses import *
from autocomplete import *
import threading

thread_cnt = 0
choices = []
choice = 0
choice_cnt = 0
lock = threading.Lock()


class RequestThread(threading.Thread):
    def __init__(self, text, pos, cnt, stdscr):
        threading.Thread.__init__(self)
        self.text = text
        self.pos = pos
        self.cnt = cnt
        self.stdscr = stdscr

    def run(self):
        global lock, choice, choice_cnt, choices, thread_cnt
        r = google(self.text, self.pos)
        if thread_cnt == self.cnt:
            lock.acquire()
            choices.clear()
            for i in r:
                if i.replace('<b>', '').replace('</b>', '') != self.text:
                    choices.append(i)
            choice_cnt = len(choices)
            choice = 0
            for i, c in enumerate(choices):
                self.stdscr.move(i + 1, 0)
                render_choice(self.stdscr, c, i == choice)
            self.stdscr.move(0, self.pos)
            self.stdscr.refresh()
            lock.release()


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
    global lock, choice, choice_cnt, choices, thread_cnt
    stdscr.clear()
    text = ''
    pos = 0
    change = False
    while True:
        k = stdscr.getch()
        change = False
        if k == KEY_DOWN:
            lock.acquire()
            if choice < choice_cnt - 1:
                choice += 1
            lock.release()
        elif k == KEY_UP:
            lock.acquire()
            if choice > 0:
                choice -= 1
            lock.release()
        elif k == KEY_LEFT:
            if pos > 0:
                pos -= 1
        elif k == KEY_RIGHT:
            if pos < len(text):
                pos += 1
        elif k == ord('\t'):
            lock.acquire()
            if choice_cnt > 0:
                text = choices[choice].replace('<b>', '').replace('</b>', '')
                pos = len(text)
                change = True
            lock.release()
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

        lock.acquire()
        stdscr.clear()
        stdscr.addstr(0, 0, text)
        stdscr.move(0, pos)
        stdscr.refresh()
        lock.release()
        if change:
            lock.acquire()
            choice = 0
            choice_cnt = 0
            choices = []
            lock.release()
            thread_cnt += 1
            thread = RequestThread(text, pos, thread_cnt, stdscr)
            thread.start()
        lock.acquire()
        for i, c in enumerate(choices):
            stdscr.move(i + 1, 0)
            render_choice(stdscr, c, i == choice)
        stdscr.move(0, pos)
        stdscr.refresh()
        lock.release()


wrapper(main)
