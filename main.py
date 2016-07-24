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
text = ''
pos = 0
scr = None


def render_choice(c, selected):
    global scr
    highlight = A_STANDOUT if selected else 0
    while c:
        p = c.find('<b>')
        q = c.find('</b>')
        if p >= 0 and p < q:
            scr.addstr(c[:p], highlight)
            scr.addstr(c[p + 3:q], A_BOLD | highlight)
            c = c[q + 4:]
        else:
            scr.addstr(c, highlight)
            break


def render_all():
    global lock, choice, choice_cnt, choices, thread_cnt, text, pos, scr
    scr.clear()
    scr.addstr(0, 0, text)
    for i, c in enumerate(choices):
        scr.move(i + 1, 0)
        render_choice(c, i == choice)
    scr.move(0, pos)
    scr.refresh()


class RequestThread(threading.Thread):
    def __init__(self, text, pos, cnt):
        threading.Thread.__init__(self)
        self.text = text
        self.pos = pos
        self.cnt = cnt

    def run(self):
        global lock, choice, choice_cnt, choices, thread_cnt, text, pos
        try:
            r = google(self.text, self.pos)
        except requests.exceptions.ReadTimeout:
            return
        if thread_cnt == self.cnt or True:
            lock.acquire()
            choice = 0
            choices.clear()
            for i in r:
                if i.replace('<b>', '').replace('</b>', '') != self.text:
                    choices.append(i)
            choice_cnt = len(choices)
            render_all()
            lock.release()


def main(stdscr):
    global lock, choice, choice_cnt, choices, thread_cnt, text, pos, scr
    scr = stdscr
    scr.clear()
    change = False
    while True:
        k = scr.getch()
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

        if change:
            thread_cnt += 1
            thread = RequestThread(text, pos, thread_cnt)
            thread.start()
        lock.acquire()
        render_all()
        lock.release()


wrapper(main)
