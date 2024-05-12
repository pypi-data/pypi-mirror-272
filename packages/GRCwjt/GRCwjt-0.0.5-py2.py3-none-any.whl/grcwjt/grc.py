#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here

import socket
import threading
import time
import SocketServer

PORT = 20005

## this is the stub implementation of getFunctions, run this in Ghidra
def getFunctions():
    ## actuall Ghidra api
    res = ""
    it = currentProgram.getFunctionManager().getFunctions(True)
    for func in it:
	res = res + "\n" + getName(func)
    return res
    
def getName(function):
    return function.getName()

def rpc_getFunctions():
    global PORT
    ## create socket client to connect the rpc server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('localhost',PORT))
    ## create a rpc object
    rpc_obj = 'getFunctions'
    ## send get function key word indicating a getFunction rpc call
    sock.sendall(rpc_obj.encode())
    ## recv the result
    msg = sock.recv(8192)
    ## deserialize the object to finally retrieve the result
    ## close the socket
    sock.close()
    ## return the actuall object
    return msg

    
## stub table
rpc_stubs = [
    ("getFunctions" , getFunctions)
]


class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Receive data from the client
        msg = self.request.recv(1024)
        print("Received data:", msg)
        if not msg:
           return
        ## if the message recved is "getfunction"
        for name,handler in rpc_stubs:
            if msg == name:
		print("execute ",msg)
                ## serialize the function result and send with socket
		msg = handler()
		print(msg)
                self.request.sendall(handler().encode())

## server starter
def start_server():
    print 'create server'
    # Define the host and port
    HOST = "localhost"
    global PORT

    # Create the server
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)

    # Start the server
    print("Server listening on {}:{}".format(HOST, PORT))
    server.serve_forever()

if __name__ == '__main__':
    ## establish a rpc server in a unique thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    time.sleep(1)
    ## make a rpc call to invoke ghidra getFunctions
    functions = rpc_getFunctions()
    print(functions)    
