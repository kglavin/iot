import time
import machine
import network
import socket

def get(url,port):
    '''do a HTTP Get using the provided url and port
       print out the received data'''
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def get_loop(url,port,count=500):
    ''' loop with a period of once per second and perform a http get operation 
         by default 500 times using the provided url and port'''
    for i in range(count):
        time.sleep_ms(999)
        get(url,port) 

def post(url,port,id,data, myhost=''):
    ''' do a HTTP POST operation, using the provided url and port, 
        a json structure is send which has 
        id: the provided unique id
        host: the host to which the data from (ip address)
        data: the provided data
        '''
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    payload='{"id":"' + id + '","host":"' + myhost +'","data":' + data +'}'
    s.send(bytes('POST /%s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: %i\r\n%s\r\n' % (path,host,len(payload),payload), 'utf8'))
    s.close()

def post_loop(url,port,count=500, sleep_time=1000):
    ''' loop with a period of 1 second, performing a HTTP post'''
    rtc = machine.RTC()
    sta_if = network.WLAN(network.STA_IF)
    myhost,_,_,_ = sta_if.ifconfig()
    idb = machine.unique_id()
    id = '{:02x}{:02x}{:02x}{:02x}'.format(idb[0], idb[1], idb[2], idb[3])
    prev_u=0
    st = 1000
    for i in range(count):
        y,mo,d,w,h,m,s,u = rtc.datetime()
        #store the subseconds to to allow calculatation of how long it takes 
        #so we can keep the period to exactly once per second.
        prev_u = u
        data = '"'+"#ts:"+str((m,s,u))+"#c1:"+str(i)+"#c2:"+str(i*i)+"#c3:"+str(i*i*i)+"#"+'"'
        post(url,port,id,data,myhost) 
        y,mo,d,w,h,m,s,u = rtc.datetime()
        st = sleep_time-(u-prev_u)
        time.sleep_ms(st)
        

while True:
    post_loop('http://192.168.2.1/data',2000,72000)

