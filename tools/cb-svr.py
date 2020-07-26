import gdb
import threading

try:
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
    from urllib import urlopen
    from urllib import urlencode


CBHOST = 'localhost'
CBPORT = 8020, 8021


class CBRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class CBRunner(object):

    def __init__(self, tid, cmd, args):
        self._tid = tid
        self._cmd = cmd
        self._args = args

    def __call__(self):
        m = getattr(gdb, self._cmd)
        r = CBProxyCommand.results.get(self._tid, {})
        if m is None:
            r['status'] = -1
            r['error'] = 'Unknown command "%s"' % self._cmd
            return

        try:
            r['value'] = m(*self._args)
            r['status'] = 0
        except Exception as e:
            r['status'] = 1
            r['error'] = str(e)


class CBProxyCommand(object):

    counter = 0
    results = {}

    def execute(self, cmd, args=None):
        self.counter += 1
        self.results[self.counter] = {'status': None}
        gdb.post_event(CBRunner(self.counter, cmd, args))
        return self.counter

    def result(self, tid=None):
        if tid is None:
            tid = self.counter
        if tid in self.results:
            ret = self.results[tid]
            if ret['status'] is not None:
                self.results.pop(tid)
            return ret


def cb_start_server(host=CBHOST, port=CBPORT[1]):
    server = SimpleXMLRPCServer((host, port),
                                requestHandler=CBRequestHandler,
                                allow_none=True)
    server.register_introspection_functions()
    server.register_instance(CBProxyCommand())
    threading.Thread(target=server.serve_forever).start()
    return server


def cb_stop_server():
    if hasattr(gdb, 'cbsvr'):
        gdb.cbsvr.shutdown()
        gdb.cbsvr.server_close()
        delattr(gdb, 'cbsvr')


def cb_exit_handler(event):
    # print "event type: exit"
    # print "exit code: %d" % (event.exit_code)
    cb_stop_server()


def cb_send_request(args, host=CBHOST, port=CBPORT[0]):
    data = urlencode(args)
    if hasattr(data, 'encode'):
        data = data.encode('ascii')
    uri = 'http://%s:%s/gdb/' % (host, port)
    with urlopen(uri, data) as f:
        return f.read().decode('utf-8')


if not hasattr(gdb, 'cbsvr'):
    gdb.cbsvr = cb_start_server()
    gdb.events.exited.connect(cb_exit_handler)
