# telnet program example
import socket, select, string, sys
import serial # if you have not already done so
import time
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600) 
    except IOError:
        time.sleep(3.0);
        ser = serial.Serial('/dev/ttyACM1', 9600)
    
    time.sleep(3.0);
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    for c in data:
                        ser.write(c)
                    #sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()