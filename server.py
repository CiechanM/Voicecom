import socket
import threading

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        #self.ip = '25.59.73.69'

        while 1:
            try:
                self.port = int(input('Wprowadz numer portu przeznaczonego dla serwera --> '))

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))

                break
            except:
                print("Nie mozna polaczyc z wybranym portem")
        self.connections = []
        self.connects = [[], []]
        self.connects[0] = []
        self.connects[1] = []
        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print('IP: '+self.ip)
        print('Port: '+str(self.port))

        while True:
            c, addr = self.s.accept()
            print(c)
            self.connections.append(c)

            threading.Thread(target=self.c_handler,
                             args=(c, addr,)).start()

    def transmission(self, sock, package, room):
        for client in self.connects[room]:
            if client != self.s and client != sock:
                try:
                    client.send(package)
                except:
                    pass
    
    def nickbroadcast(self, sock, nickname, room):
         for client in self.connects[room]:
            if client != self.s and client != sock:
                try:
                    client.send(nickname + " dolaczyl/a do pokoju nr " + room)
                except:
                    pass

    def c_handler(self, c, addr):

        message = c.recv(1024)
        message = message.decode()
        room = int(message[0])

        nick = message[1:]
        print(str(nick) + " dolaczyl/a do pokoju nr " + str(room))

        self.connects[room].append(c)

        while 1:
            try:
                package = c.recv(1024)
                self.transmission(c, package, room)

            except socket.error:
                c.close()

server = Server()
