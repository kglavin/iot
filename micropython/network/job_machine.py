import time
import requests
import json

class JobMachine:
    ttl = 0
    valid_op_codes = [ 'default']

#    default_job_dict = {
#        #  opcode  --  (function, jump_ok_func, ok_next, jump_nok_func, nok_next, time_budget, ttl
#        'default': {'func':'do_config',
#                    'val':{'url':'http://192.168.2.1:2000/config'}, 
#                    'ttl': 20, 
#                    'valid_op_codes':[ 'default']}
#    }

    job_dict = {}

    def run(self, opcode='default', num_loops=1):
        if len(self.job_dict) == 0:
            print('run do_config first')
            return 'nok-run_do_config'
        loop_opcode=opcode
        for j in range(0,num_loops):
            print("loop: ",j)
            opcode = loop_opcode
            self.ttl = self.job_dict[opcode]['ttl']
            for x in range(0,len(self.job_dict)):
                if opcode in self.valid_op_codes:
                    self.ttl -= 1
                    if (self.ttl > 0) :
                        func = self.job_dict[opcode]['func']
                        val = self.job_dict[opcode]['val']
                        term = getattr(self,func)
                        print('op['+str(opcode)+"] func["+func+"] val["+str(val)+"] ttl["+str(self.ttl)+']')  
                        ret = term(val)
                        print('                 ret: ',ret)

                        if ret == 'ok':
                            if opcode == 'default':
                                self.ttl = self.job_dict[opcode]['ttl']
                                opcode = '1'
                            else:
                                if opcode == len(self.job_dict)-1:
                                    opcode='default'
                                else:
                                    t = int(opcode)
                                    opcode = str(t+1)
                        else: 
                            print('     op: '+ str(opcode) + 'returned nok -- restarting at default')
                            opcode='default'

                    else:
                        print('ttl expired:', opcode)
                        return 'nok'

                    # if we are back at default then lets reset the ttl and go again
                    if opcode == 'default':
                        self.ttl = self.job_dict[opcode]['ttl']
                else:
                    print("opcode not recognised",opcode)
                    print(self.job_dict)
                    return 'nok'

    def do_config(self,val={}):
        print("     do_config:",val)
        id = '70a1b200'
        r = requests.get('http://192.168.2.1:2000/config/'+id)
        if r.status_code == 200:
            self.job_dict = json.loads(r.text)
            self.valid_op_codes = self.job_dict['default']['valid_op_codes']
        return 'ok'

class StatsMachine(JobMachine):

    def do_stat(self,val={}):
        print("     do_stat",val)
        u_id = '70a1b200'
        gateway_url = 'http://192.168.2.1:2000/'
        ds = dict()
        ds['xvib'] = 3500 
        ds['yvib'] = 27000
        ds['hfac'] = 2.45
        ds['rpm']  = 5600
        ds['temp'] = 55
        ds['ts'] = str((1,2,3))
        ds['id'] = u_id
        ds['sub'] = 42
        ds['indx'] = 1
        dd=dict()
        dd['data'] = ds
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(gateway_url+'data/'+u_id,data=json.dumps(dd), headers=headers)
        print("post: %s %s " %( ds['indx'],r.status_code))
        return 'ok'

    def do_sleep(self,val={}):
        print('     do_sleep',val)
        time.sleep(1)
        return 'ok'

    def do_inc_ttl(self,val={}):
        ttl = 0
        if 'ttl' in val:
            ttl = val['ttl'] 
        print('     do_inc_ttl',val)
        self.ttl += ttl
        return 'ok'

    def do_nop(self,val={}):
        print('     do_nop',val)
        return 'ok'


my_job = StatsMachine()
my_job.do_config()
my_job.run(num_loops=500)

