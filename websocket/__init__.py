#coding=utf-8

from . import WebSocketServer
import threading, socket

testsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = testsock.connect_ex(('127.0.0.1', 9999))
if not result == 0:
	server = WebSocketServer.WebsocketServer()
	serverThread = threading.Thread(target=server.start)
	serverThread.start()
else:
	testsock.close()
