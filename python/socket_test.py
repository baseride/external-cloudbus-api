# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory, connectWS
import thread
import json
from twisted.internet import reactor

CLIENT_TOKEN = 'enter your client access token'

class CloudbusClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        self.factory.web_socket = self

    def onOpen(self):
        print 'Start oauth'
        self.sendMessage( json.dumps({'kind':'oauth', 'token':CLIENT_TOKEN}) )

    def onClose(self, wasClean, code, reason):
        print 'Close connect; clean='+str(wasClean)+' code:'+str(code)+' reason:'+str(reason)

    def onServerConnectionDropTimeout(self):
        print 'ServerConnectionDropTimeout'

    def onPing(self, payload):
        self.sendPong(payload)
    #def onPong(self, payload):
    #    print "Pong received"

    def onMessage(self, payload, isBinary):

        msg = json.loads(payload)

        print 'MSG: '+str(msg)

        if msg['kind']=='oauth':
            print 'OAUTH '+str(msg['user'])

            ent = 162 # Demo Cloudbus enterprise Id

            # subscribe to all events 'vehicle enter to area' :
            jsub = { 'kind':'subscribe', 'subscribe':{'enterprise':ent, 'kind':'area_enter', 'type':'transport.vehicle', 'id':0} }
            self.sendMessage( json.dumps(jsub) )

            self.setTrackTimings(True)
            print 'Start listen'

        elif msg['kind']=='data':
            itm = str(msg['tag']['id'])+": "+str(msg['tag']['kind']+" "+msg['tag']['type'])
            print 'DATA: '+str(itm)


def ping_pong():
    # test_factory.factory.web_socket.sendPing()
    reactor.callLater(100, ping_pong)


###
test_factory = WebSocketClientFactory(
    'wss://baseride.com/sockjs/websocket',
    debug=True,
    debugCodePaths=True)
test_factory.protocol = CloudbusClientProtocol
connectWS(test_factory)

reactor.callWhenRunning(ping_pong)
reactor.run()
