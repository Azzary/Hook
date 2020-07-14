from threading import Thread
import socket, time, fritm



class MITM():
    def __init__(self,server_ip = "127.0.0.1",server_port = 6555, var = True):
        self.server_port = server_port
        self.server_ip = server_ip
        if var: 
            self._hook()
        self.start_client(server_ip,server_port)


    def start_client(self, server_ip, server_port):
        self.socket_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_to_client.bind((server_ip,server_port))
        except:
            print(f"Can't blind for the client")

        self.socket_to_client.listen(1)
        self.connexion, adresse, = self.socket_to_client.accept()
        print("connection made...\nconnection to server")
        
        self.listening_client()


    def start_server(self,adresse):
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_to_server.connect((adresse[0],int(adresse[1])))
            self.connexion.send((f"HTTP/1.0 200 OK").encode())
            time.sleep(0.5)
        except:
            print(f"Can't blind the server")

        #listening_server
        Thread(None,self._boucle_recv_send,args = [self.socket_to_server, self.connexion, "Server: "]).start()    


    def listening_client(self):
        #packet contains the true ip and port 
        packet = self.connexion.recv(1024).decode()
        packet = packet.split(" ")[1].split(":")
        self.start_server(packet)
        self._boucle_recv_send( self.connexion, self.socket_to_server, "Client: ")                  
        self._switch_server()

    def _switch_server(self):
        self.socket_to_server.close()
        self.socket_to_client.close()
        self.connexion.close() 
        Thread(None,self.__init__,args = [self.server_ip,self.server_port, False]).start()    

    def _hook(self):
        fritm.spawn_and_hook("D:/Program Files (x86)/Ankama/retro/resources/app/retroclient/Dofus.exe", 6555)
        self.httpd = fritm.start_proxy_server(None)

    def _boucle_recv_send(self, recv, send, source, packets = None):
        while packets != "":
            try:
                packets = recv.recv(1024)
                send.send(packets)
            except:
                break
            packets = packets.decode()
            print(packets)

  

            
        recv.close()
        print("close connection with a "+ source) 

if __name__ == "__main__":
    MITM()