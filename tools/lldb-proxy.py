#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
This script is used to connect LLDB and CodeBang by websocket.

Note:

  In MacOS if lldb is installed within XCode, start any command with `xcrun`

  First install package `websockets`

    xcrun pip3 install websockets

  Then start server

    xcrun python3 lldb-proxy.py

  Refer to
  https://lldb.llvm.org/resources/caveats.html#lldb-in-xcode-on-macos

"""

import asyncio
import json
import logging
import os
import sys
import websockets

from threading import Thread

try:
    import lldb
except ImportError:
    sys.path.append('/Applications/Xcode.app/Contents/SharedFrameworks/'
                    'LLDB.framework/Resources/Python3')
    import lldb


class Debugger(object):

    def __init__(self):
        self.debugger = lldb.SBDebugger.Create()
        self.debugger.SetAsync(False)
        self.target = None

    def handle_command(self, command):
        name = command.get('name')
        action = command.get('action')
        args = command.get('args')

        obj = self if name == 'debugger' else getattr(self, name)
        if obj is not None and callable(name):
            obj = obj()
        if obj is None:
            raise RuntimeError('No %s found' % name)

        m = getattr(obj, action)
        if m is None:
            raise RuntimeError('No method %s found' % action)

        return m(*args)

        # self.debugger.HandleCommand(command)

    def _add_breakpoint(self, bp=None):
        main_bp = self.target.BreakpointCreateByName(
            "main", self.target.GetExecutable().GetFilename())
        print(main_bp)

    def _disassemble(self, insts):
        for i in insts:
            print(i)

    def load(self, filename):
        self.target = self.debugger.CreateTargetWithFileAndArch(
            filename, lldb.LLDB_ARCH_DEFAULT)

        if not self.target:
            raise RuntimeError('Load %s failed' % filename)

    def launch(self):
        process = self.target.LaunchSimple(None, None, os.getcwd())
        if process:
            state = process.GetState()
            if state == lldb.eStateStopped:
                thread = process.GetThreadAtIndex(0)
                if thread:
                    frame = thread.GetFrameAtIndex(0)
                    if frame:
                        function = frame.GetFunction()
                        if function:
                            insts = function.GetInstructions(self.target)
                            self._disassemble(insts)
                        else:
                            symbol = frame.GetSymbol()
                            if symbol:
                                print(symbol)


def handler(ws, cid, command, options):
    result = {}
    result['id'] = cid
    result['code'] = 0

    try:
        result['result'] = debugger.handle_command(command)
    except Exception as e:
        result['code'] = -2
        result['result'] = e

    ws.send(json.dumps(result))


def parse_message(message):
    data = json.loads(message)
    if not isinstance(data, list):
        raise RuntimeError('message is not a list')
    if len(data) == 2:
        data.append({})
    if len(data) != 3:
        raise RuntimeError('there is more than 3 items in the message')
    return data


async def receiver(websocket, path):
    logging.info('Start receiver for %s ...', websocket.remote_address)
    try:
        async for message in websocket:
            logging.info("Receive message: %s", message)
            try:
                data = parse_message(message)
            except Exception as e:
                websocket.send(json.dumps({
                    'cid': -1,
                    'code': -1,
                    'result': e
                }))
                logging.info("Invalid Message: %s", e)
                continue

            cid, command, options = data
            if options.get('async'):
                logging.info("Got async event %s", cid)
                Thread(target=handler,
                       args=(websocket, cid, command, options)).start()
                logging.info("Async Event %s dispatched", cid)
            else:
                logging.info("Got event %s", cid)
                handler(websocket, cid, command, options)
                logging.info("Event %s end", cid)
    finally:
        logging.info('Quit receiver for %s.', websocket.remote_address)


def start_server(host='localhost', port=6789):
    server = websockets.serve(receiver, host, port)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(thread)x] %(message)s")
    debugger = Debugger()
    host, port = 'localhost', 6789
    try:
        logging.info('Start server at %s:%s...', host, port)
        start_server()
    except KeyboardInterrupt:
        logging.info('Quit server from %s:%s...', host, port)
