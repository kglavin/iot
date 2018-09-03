#iotstats.py
#
# generate statistics on IOT thing and send via http to iot gateway
#

import usocket
import urequests as requests
import time
import machine
import network
import json



def do_stats(loops=1000):
    gateway_url = "http://192.168.2.1:2000/"
    count=1
    sta_if = network.WLAN(network.STA_IF)
    myhost,_,_,_ = sta_if.ifconfig() 
    m_id = machine.unique_id()
    u_id = '{:02x}{:02x}{:02x}{:02x}'.format(m_id[0], m_id[1], m_id[2], m_id[3])
    rtc = machine.RTC()

    r = requests.get(gateway_url+'config/'+u_id)
    default_configs = {'loop':1000, 'stat_loop':20 } 
    try:
        if r.status_code == 200:
            configs = json.loads(r.text)
        else:
            configs = default_configs
    except:
        print("got KeyError on config JSON")
        configs = default_configs
    r.close()

    loop = configs['loop']
    stats_loop = configs['stat_loop']
    
    for c in range(loop):
    	r = requests.get(gateway_url+'config/'+u_id)
        print(r.status_code, c, r.text)
        r.close()
        for p in range(stats_loop):
            try:
                y,mo,d,w,h,m,s,u = rtc.datetime()
                ds = dict()
                ds['xvib'] = 3500 
                ds['yvib'] = 27000
                ds['hfac'] = 2.45
                ds['rpm']  = 5600
                ds['temp'] = 55
                ds['ts'] = str((m,s,u))
                ds['id'] = u_id
                ds['sub'] = 42
                ds['indx'] = count = count+1
                dd=dict()
                dd['data'] = ds
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(gateway_url+'data/'+u_id,data=json.dumps(dd), headers=headers)
                print("post: %s %s " %( ds['indx'],r.status_code))
                time.sleep_ms(300)
                r.close()
            except OSError:
                print('Caught OSError')

do_stats()