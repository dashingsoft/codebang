import gdb
import threading

try:
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
except ImportError:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Runner(object):

    def __init__(self, tid, cmd, args):
        self._tid = tid
        self._cmd = cmd
        self._args = args

    def __call__(self):
        m = getattr(gdb, self._cmd)
        r = ProxyCommand.results.get(self._tid, {})
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


class ProxyCommand(object):

    counter = 0
    results = {}

    def execute(self, cmd, args=None):
        self.counter += 1
        self.results[self.counter] = {'status': None}
        gdb.post_event(Runner(self.counter, cmd, args))
        return self.counter

    def result(self, tid=None):
        if tid is None:
            tid = self.counter
        if tid in self.results:
            ret = self.results[tid]
            if ret['status'] is not None:
                self.results.pop(tid)
            return ret


def cb_start_server(host='localhost', port=8000):
    server = SimpleXMLRPCServer((host, port),
                                requestHandler=RequestHandler,
                                allow_none=True)
    server.register_introspection_functions()
    server.register_instance(ProxyCommand())
    threading.Thread(target=server.serve_forever).start()
    return server


def cb_stop_server():
    if hasattr(gdb, 'cbsvr'):
        gdb.cbsvr.shutdown()
        delattr(gdb, 'cbsvr')


if not hasattr(gdb, 'cbsvr'):
    gdb.cbsvr = cb_start_server()
