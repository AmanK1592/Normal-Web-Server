import socket
import threading
import sys
from urlparse import urlparse
import urllib
import subprocess
import StringIO
import gzip

host1 = ''
port1 = int(sys.argv[1])                                                                                                #Command line input for port


class ThreadedServer(object):                                                                                           #Multithreaded Web Server

    def __init__(self, host, port):                                                                                     #Establishing a socket connection
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print"New Thread started for "+str(port)

    def listen(self):
        self.sock.listen(4)
        while True:
            client_sock, client_address = self.sock.accept()
            threading.Thread(target=self.listentoClient, args=(client_sock, client_address)).start()

    def listentoClient(self, client_sock, client_address):                                                              #Listening on a port for incoming connections
        size = 1024
        while True:

            try:
                data = client_sock.recv(size)
                if data:
                    #data = r
                    #client_sock.send(data)
                    request = (data.splitlines())
                    full_command = request[0]
                    url = full_command.split(' ')
                    #print url[1]

                    if "HTTP/1.1" in url[2]:                                                                            #Check if the request is HTTP v1.1 else return a 404 error

                        if "GET" in url[0]:                                                                             #Check if request is a valid GET request else return a 404 error
                            command = urlparse(url[1])
                            path = command.path
                            path = urllib.unquote(path)

                            #path = path.replace("%20", " ")
                            print path

                            if "/exec/" in path:                                                                        #Check for exec in the whole path  else return a 404
                                path1, prompt = path.split("/exec/", 1)
                                print path1
                                print prompt

                                prompt = urllib.unquote(prompt)
                                #prompt = prompt.replace("%20", " ")
                                #print prompt
                                #client_sock.send(prompt)
                                #client_sock.send('\n')

                                if "vim" in prompt:                                                                     #Check for Vim command in the command line
                                    o = "Command Executed !"
                                    client_sock.send("HTTP/1.1 200 OK\r\n"+"Content-Type: text/plain\n"+"\r\n" + o)
                                    #client_sock.close()
                                else:
                                    if "curl" in prompt:                                                                #Check for curl in command line
                                        curl, ext = prompt.split(" ", 1)
                                        ext = ext.replace(" ", "%20")
                                        c1 = curl + " " + ext

                                        subp = subprocess.Popen(c1, stdout=subprocess.PIPE, shell=True)                 #Execute the Linux Syscall
                                        (cout, cerr) = subp.communicate()
                                        o1 = str(cout)
                                        client_sock.send("HTTP/1.1 200 OK\r\n" + "Content-Type: text/plain\r\n" + "Content-Length: 3495\n" "\r\n" + o1)
                                        #client_sock.close()


                                    else:
                                        op = subprocess.Popen(prompt, stdout=subprocess.PIPE, shell=True)
                                        (output, err) = op.communicate()
                                        print output
                                        client_sock.send("HTTP/1.1 200 OK\r\n" + "Content-Type: text/plain\r\n" + "Content-Length: 3495\n" "\r\n" + output)
                                        client_sock.close()

                                    #out = StringIO.StringIO()                                                          #Gzip Encoding
                                    #with gzip.GzipFile(fileobj=out, mode="w") as f:
                                    #    f.write(output)
                                    #p = out.getvalue()
                                    #final = str(p)
                                    #ln = len(p)
                                    #print p
                                    #print final
                                    #print ln

                                    #client_sock.send("HTTP/1.1 200 OK\r\n" + "Content-Type: text/plain\r\n" + "Content-Encoding: gzip\r\n" + "Content-Length: " + str(ln) + "\r\n\r\n" + final + "\r\n")
                                    #client_sock.close()
                            else:
                                a = "Command Not Found!"

                                client_sock.send("HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/plain\r\n" + "Content-Length: 3495\n" + "\r\n" + a)
                                #client_sock.close()
                        else:
                            b = "404: Invalid Request"

                            client_sock.send("HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/plain\r\n" + "Content-Length: 3495\n" + "\r\n" + b)
                            #client_sock.close()
                    else:
                        c = "404: Invalid Request"

                        client_sock.send("HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/plain\r\n" + "Content-Length: 3495\n" + "\r\n" + c)
                        #client_sock.close()
                client_sock.close()
            except:

                client_sock.close()
                return False

if __name__ == "__main__":
    ThreadedServer(host1, port1).listen()

