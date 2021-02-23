# -*- coding: utf-8 -*-
'''GDB Extension
'''
import gdb
import threading

from urllib.request import urlopen
from urllib.parse import urlencode


cb_notify_url = 'http://localhost:20829/api/v1/event/gdb/'


def cb_post_event(runner, pk=None):
    if cb_lock.acquire(timeout=1.0):
        runner()
        cb_lock.release()
    elif pk is not None:
        cb_notify_event({
            'pk': pk,
            'error': 'Timeout'
        })


def cb_execmd(*cmdlist):

    def _runner():
        for cmd in cmdlist:
            gdb.execute(cmd)
        gdb.flush()

    cb_post_event(_runner)


def cb_prog_begin(pk, filename):

    def _runner():
        i = gdb.selected_inferior()
        if i.progspace.filename is not None:
            res = gdb.execute('add-inferior -no-connection', False, True)
            n = res.split()[-1]
            gdb.execute('inferior %s' % n)
        gdb.execute('set remote exec-file %s' % filename)
        gdb.execute('file %s' % filename)
        gdb.flush()

        cb_notify_event({
            'pk': pk,
            'inferior': i.num,
            'filename': filename
        })

    cb_post_event(_runner)


def cb_prog_end(pk, num):

    def _runner():
        gdb.execute('kill inferiors %s' % num)
        gdb.execute('detach inferior %s' % num)
        if num > 1:
            if gdb.selected_inferior().num == num:
                gdb.execute('inferior 1')
            gdb.execute('remove-inferiors %s' % num)
        gdb.flush()

        cb_notify_event({
            'pk': pk,
        })

    cb_post_event(_runner)


def cb_prog_cmd_async(pk, cmd, arg='', thread=None):
    # run / step / stepi / next / nexti / continue / until / finish &
    cmdlist = [] if thread is None else ['thread apply', thread, '-s']
    cmdlist.extend([cmd, arg, '&'])

    def _runner():
        result = gdb.execute(' '.join(cmdlist), False, True)
        cb_notify_event({
            'pk': pk,
            'result': result
        })

    cb_post_event(_runner)


def cb_prog_cmd(pk, cmd, arg='', thread=None, frame=None):
    # -stack-list-variables --thread 1 --frame 0 --all-values
    # ^done,variables=[{name="x",value="11"},{name="s",value="{a = 1, b = 2}"}]

    # -stack-list-frames --thread 1
    # ^done,stack=
    # [frame={level="0",addr="0x0001076c",func="foo",
    #  file="recursive2.c",fullname="/home/foo/bar/recursive2.c",line="11",
    #  arch="i386:x86_64"},
    #  ...]

    # -stack-list-arguments --thread 1 1
    # ^done,
    # stack-args=[
    # frame={level="0",args=[]},
    # ...]

    # -thread-info
    # -thread-list-ids

    # -data-disassemble
    # -data-evaluate-expression expr
    # -data-list-changed-registers
    # -data-list-register-names
    # -data-list-register-values

    # -data-read-memory
    # -data-read-memory-bytes
    # -data-write-memory-bytes

    # -symbol-info-functions
    # -symbol-info-module-functions
    # -symbol-info-module-variables
    # -symbol-info-modules
    # -symbol-info-types
    # -symbol-info-variables

    # -exec-continue
    # -exec-finish
    # -exec-interrupt
    # -exec-next
    # -exec-next-instruction
    # -exec-return
    # -exec-run --start
    # -exec-step
    # -exec-step-instruction
    # -exec-until

    # -break-insert
    # -break-delete
    # -break-condition
    # -break-list
    # -break-info
    # -break-disable
    # -break-enable
    # -break-watch

    cmdlist = ['interpreter-exec mi', '"', cmd]
    if thread is not None:
        cmdlist.extend(['--thread', thread])
    if frame is not None:
        cmdlist.extend(['--frame', frame])
    cmdlist.extend([arg, '"'])

    def _runner():
        result = gdb.execute(' '.join(cmdlist), False, True)
        cb_notify_event({
            'pk': pk,
            'result': result
        })

    cb_post_event(_runner)


def cb_dispatch(pk, cmd, *args):
    if cmd == 'prog_begin':
        cb_prog_begin(pk, *args)
    elif cmd == 'prog_end':
        cb_prog_end(pk, *args)
    elif cmd == 'prog_cmd':
        cb_prog_cmd(pk, *args)
    elif cmd == 'prog_cmd_async':
        cb_prog_cmd_async(pk, *args)


def cb_new_inferior_handler(event):
    event.inferior


def cb_exited_handler(event):
    event.inferior, event.exit_code


def cb_new_thread_handler(event):
    thread = event.inferior_thread
    if isinstance(thread, gdb.Inferior):
        cb_notify_event({
            'inferior': thread.num,
            'state': 'new',
        })
    else:
        cb_notify_event({
            'inferior': thread.inferior.num,
            'thread': thread.num,
            'gthread': thread.global_num,
            'state': 'new',
        })


def cb_stop_handler(event):
    thread = event.inferior_thread
    gdb.write('stop_handler: %s' % type(thread))
    if hasattr(event, 'breakpoints'):
        reason = [(bp.thread, bp.number, bp.type, bp.location)
                  for bp in event.breakpoints]
    elif hasattr(event, 'stop_signal'):
        reason = event.stop_signal
    else:
        reason = ''

    if isinstance(thread, gdb.Inferior):
        cb_notify_event({
            'inferior': thread.num,
            'state': 'exited' if thread.is_exited() else 'stopped',
            'reason': reason
        })
    else:
        cb_notify_event({
            'inferior': thread.inferior.num,
            'thread': thread.num,
            'gthread': thread.global_num,
            'state': 'exited' if thread.is_exited() else 'stopped',
            'reason': reason
        })


def cb_cont_handler(event):
    thread = event.inferior_thread
    cb_notify_event({
        'inferior': thread.inferior.num,
        'thread': thread.num,
        'state': 'running',
    })


def cb_notify_event(args):
    data = urlencode(args)
    r = urlopen(cb_notify_url, data.encode('ascii'))
    if r.status == 200:
        return r.read().decode('utf-8')


#
# Hook event
#
# gdb.events.new_inferior.connect(cb_new_inferior_handler)
# gdb.events.exited.connect(cb_exited_handler)
# gdb.events.cont.connect(cb_cont_handler)

gdb.events.new_thread.connect(cb_new_thread_handler)
gdb.events.stop.connect(cb_stop_handler)

cb_lock = threading.Lock()
