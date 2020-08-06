# SEAN TOBE

import socketserver
import queue
import re
import time

# make a queue
q = queue.Queue()
# add some dark conversation starters - don't worry, he will not bother us for long
name = "sad sack"
sadsack_says = [ \
    "Hi subway, what do you do", \
    "Ill start a sub", \
    "ill have a huge size", \
    "i want wheat bread", \
    "order turkey, tuna, ham", \
    "add spinach, mushys, peppers", \
    "i need oil over the top please", \
    "i like toasted!", \
    "confirm", \
    "start sub" ]
for depressives in sadsack_says:
    q.put(name + "|MiPik|" + depressives)

#test = name + "|everyone|" + sadsack_says[0]
#print(test)
regex = re.compile(r'^.+\|.+\|.+$') # can you figure out what the matches;-)
#if regex.match(test):
#    print("ok")

class ChatHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            data = self.request[0].strip() # data is a byte object
            socket = self.request[1]
            # expects to get three pipe separated values with name|to|chat message
            if regex.match(str(data)): # input validation
                name, to, message = data.decode().strip().split('|')
		# add some limits
                name = name[0:16]
                to = to[0:16]
                message = message[0:2016]
                # returns the previous chats from other servers 
                socket.sendto(("\n".join(list(q.queue)) + "\n").encode(), self.client_address)
		# add to the q and delete oldest
                q.put("|".join((name, to, message)))
                q.get() # removing old
		# print the message in local shell to show ongoing chat
                print(name + " @" + to + ": " + message)

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), ChatHandler)
    server.serve_forever()
