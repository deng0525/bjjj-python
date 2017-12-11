###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################
import json

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

# identify/translate
# {
#     'type': 'client'
#     'from': self.peer
#     'to'  : 'bjjj-javascript'
#     'msg' : {'key': 'value'}
# }
#######################
# identify/translate to peer
# {
#     'type': 'javascript'
#     'from': self.peer
#     'to'  : peer
#     'msg' : {'key': 'value'}
# }

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            # print("Binary message received: {0} bytes".format(len(payload)))

            # echo back message verbatim
            self.sendMessage(payload, isBinary)
            pass
        else:
            # print("Text message received: {0}".format(payload.decode('utf8')))
            # json
            try:
                data = json.loads(payload.decode('utf8'))
                type = data['type']
                # server received msg from client/javascript, needs to make from-peer seen in server...
                data['from'] = self.peer
                if type and type == 'javascript':
                    if self.factory.bjjj_js is None:
                        self.factory.bjjj_js = self
                    if data.get('to') and data.get('msg'):
                        to_peer = data['to']
                        client = self.factory.clients[to_peer]
                        if client:
                            client.sendMessage(json.dumps(data).encode('utf8'))
                        print("Translate javascript msg to peer: {0}".format(to_peer))
                elif type and type == 'client':
                    if self.factory.bjjj_js is None:
                        result = {}
                        result['type'] = 'javascript'
                        result['from'] = None
                        result['to'] = self.peer
                        result['msg'] = {'rescode': '500', 'resdesc': 'javascript un-founded'}
                        self.sendMessage(json.dumps(result).encode('utf8'))
                        print("Translate error result to peer: {0}".format(self.peer))
                    else:
                        self.factory.bjjj_js.sendMessage(json.dumps(data).encode('utf8'))
                        print("Translate msg to javascript from peer: {0}".format(self.peer))
            except:
                pass

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.unregister(self)

class RouterFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(RouterFactory, self).__init__(*args, **kwargs)
        self.clients = {}
        self.bjjj_js = None

    def register(self, client):
        """client register"""
        self.clients[client.peer] = client

    def unregister(self, client):
        """client unregister"""
        del self.clients[client.peer]
        if self.bjjj_js == client:
            self.bjjj_js = None


if __name__ == '__main__':
    import asyncio

    factory = RouterFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
