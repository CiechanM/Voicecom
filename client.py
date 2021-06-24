import pyaudio
import socket
import threading

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        chunk_size = 1024 
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recstream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

    def connect(self, ipAddress, port):
        while 1:
            try:
                self.target_ip = ipAddress
                self.target_port = int(port)
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Nie mozna polaczyc sie z serwerem")

    def room_pick(self, roomNumber, nickname):
        self.nickname = nickname
        message = str(roomNumber)
        message = message + str(nickname)
        message = message.encode()
        self.s.send(message)
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_to_server(self):
        while True:
            try:
                package = self.recstream.read(1024)
                self.s.sendall(package)
            except:
                pass

client = Client()
