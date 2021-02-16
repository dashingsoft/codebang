# -*- coding: utf-8 -*-
'''GDB Extension

'''
import gdb

from urllib.request import urlopen
from urllib.parse import urlencode


CBURL = 'http://localhost:20929/api/v1/event/gdb/'


def execmd(*cmdlist):

    def _runner():
        for cmd in cmdlist:
            gdb.execute(cmd)

    gdb.post_event(_runner)


def startprog(filename):

    def _runner():
        i = gdb.selected_inferior()
        if i.is_valid() and i.progspace.filename is None:
            gdb.execute('set remote exec-file ' + filename)
        else:
            res = gdb.execute('add-inferior -no-connection', False, True)
            n = res.split()[-1]
            gdb.execute('inferior ' + n)
            gdb.execute('set remote exec-file ' + filename)
        cb_notify_event({
            'event': 'new_inferior',
            'num': i.num,
            'filename': filename
        })

    gdb.post_event(_runner)


def cb_new_inferior_handler(event):
    event.inferior


def cb_exited_handler(event):
    event.inferior, event.exit_code


def cb_stop_handler(event):
    event.stop_signal, event.breakpoints


def cb_cont_handler(event):
    event.inferior_thread


def cb_notify_event(args):
    data = urlencode(args)
    r = urlopen(CBURL, data.encode('ascii'))
    if r.status == 200:
        return r.read().decode('utf-8')


#
# Hook event
#
gdb.events.new_inferior.connect(cb_new_inferior_handler)
gdb.events.exited.connect(cb_exited_handler)
gdb.events.stop.connect(cb_stop_handler)
gdb.events.cont.connect(cb_cont_handler)
