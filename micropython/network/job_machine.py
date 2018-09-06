import time

class JobMachine:
    ttl = 0

    job_dict = {
        #  opcode  --  (function, jump_ok_func, ok_next, jump_nok_func, nok_next, time_budget, ttl
        'default': {'func':'do_config',
                    'val':'url=http://192.168.2.1:2000/config', 
                    'ttl': 20, 
                    'valid_op_codes':[ 'default',1,2,3,4,5,6,7]},
        1:        {'func':'do_stat',
                    'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
        2:        {'func':'do_sleep',
                    'val':{'time':200}},
        3:        {'func':'do_stat',
                    'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
        4:        {'func':'do_sleep',
                    'val':{'time':200}},
        5:        {'func':'do_stat',
                    'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
        6:        {'func':'do_sleep',
                    'val':{'time':200}},
        7:        {'func':'do_inc_ttl',
                    'val':{'ttl':7}},
    }

    def run(self, opcode='default'):
        next_opcode='default'
        self.ttl = self.job_dict[opcode]['ttl']

        while True:
            if opcode in self.job_dict:
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
                            opcode = 1
                            print('(d:1)')
                        else:
                            if opcode == len(self.job_dict)-1:
                                opcode='default'
                                print('(%i:1)'%len(self.job_dict))
                            else:
                                opcode +=1
                                print('(n:n+1)')
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
                print("opcode not recognised",opcode, next_opcode, )
                return 'nok'


    def do_config(self,val={}):
        print("     config:",val)
        return 'ok'
  

    def do_stat(self,val={}):
        print("     do_stat",val)
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

my_job = JobMachine()
my_job.run()

