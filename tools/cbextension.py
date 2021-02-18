# -*- coding: utf-8 -*-
'''GDB Extension

'''
import gdb
import threading

from urllib.request import urlopen
from urllib.parse import urlencode


CBURL = 'http://localhost:20829/api/v1/event/gdb/'


def post_event(runner):
    if not lock.acquire(timeout=1.0):
        return None
    runner()
    lock.release()


def execmd(*cmdlist):

    def _runner():
        for cmd in cmdlist:
            gdb.execute(cmd)
        gdb.flush()

    post_event(_runner)


def prog_begin(filename, pk):

    def _runner():
        i = gdb.selected_inferior()
        if i.is_valid() and i.progspace.filename is None:
            gdb.execute('set remote exec-file %s' % filename)
        else:
            res = gdb.execute('add-inferior -no-connection', False, True)
            n = res.split()[-1]
            gdb.execute('inferior %s' % n)
            gdb.execute('set remote exec-file %s' % filename)
        gdb.flush()
        cb_notify_event({
            'event': 'begin_prog',
            'pk': pk,
            'num': i.num,
            'filename': filename
        })

    post_event(_runner)


def prog_end(num):

    def _runner():
        gdb.execute('kill inferiors %s' % num)
        gdb.execute('detach inferior %s' % num)
        if num > 1:
            if gdb.selected_inferior().num == num:
                gdb.execute('inferior 1')
            gdb.execute('remove-inferiors %s' % num)
        gdb.flush()

    post_event(_runner)


def prog_cmd(num, *cmdlist):

    def _runner():
        gdb.execute('inferior %s' % num)
        for cmd in cmdlist:
            gdb.execute(cmd)
        gdb.flush()

    post_event(_runner)


def cb_new_inferior_handler(event):
    pass # event.inferior


def cb_exited_handler(event):
    pass # event.inferior, event.exit_code


def cb_stop_handler(event):
    pass # event.stop_signal, event.breakpoints


def cb_cont_handler(event):
    pass # event.inferior_thread


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

lock = threading.Lock()
