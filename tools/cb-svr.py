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
        ProxyCommand.results[self._tid] = m(self._args)


class ProxyCommand(object):

    counter = 0
    results = {}

    def execute(self, cmd, args):
        self.counter += 1
        gdb.post_event(Runner(self.counter, cmd, args))
        return self.counter

    def result(self, tid):
        return self.results.pop(tid) if tid in self.results else None


def start_server(host='localhost', port=8000):
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_instance(ProxyCommand())
    threading.Thread(target=server.serve_forever).start()
    return server


def stop_cb_server():
    if cbsvr:
        cbsvr.shutdown()


cbsvr = start_server()
