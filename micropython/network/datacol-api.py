import sys

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

things = {}
configs = { '70a1b200':  {  1:        {'func':'do_stat',
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
                            8:        {'func':'do_sleep',
                                        'val':{'time':200}},
                            9:        {'func':'do_stat',
                                        'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
                            10:        {'func':'do_stat',
                                        'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
                            'default': {'func':'do_config',
                                        'val':{'url':'http://192.168.2.1:2000/config/1'}, 
                                        'ttl': 20, 
                                        'valid_op_codes':['1','2','3','4','5','6','7','8','9','10','default']}
                            },
                            '38ac5800':  {  1:        {'func':'do_stat',
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
                            8:        {'func':'do_sleep',
                                        'val':{'time':200}},
                            9:        {'func':'do_stat',
                                        'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
                            10:        {'func':'do_stat',
                                        'val':{'url':'http://192.168.2.1:2000/stats/<id>'}},
                            'default': {'func':'do_config',
                                        'val':{'url':'http://192.168.2.1:2000/config/1'}, 
                                        'ttl': 20, 
                                        'valid_op_codes':['1','2','3','4','5','6','7','8','9','10','default']}
                            }
            }  

def abort_if_thing_doesnt_exist(thing_id):
    if thing_id not in things:
        abort(404, message="IOT Device {} doesn't exist".format(thing_id))

def abort_if_config_doesnt_exist(id):
    if id not in configs:
        abort(404, message="IOT device {} doesn't exist".format(id))

parser = reqparse.RequestParser()
parser.add_argument('data',location='json', required=True)
parser.add_argument('id',location='json')

class Thing(Resource):

    def __init__(self):
        self.count=1

    def get(self, thing_id):
        abort_if_thing_doesnt_exist(thing_id)
        return things[thing_id]

    def delete(self, thing_id):
        abort_if_thing_doesnt_exist(thing_id)
        del things[thing_id]
        return '', 204

    def put(self, thing_id):
        args = parser.parse_args()
        data = {'data': args['data']}
        things[thing_id] = data
        return data, 201

    def post(self, thing_id):
        args = parser.parse_args()
        data = {'data': args['data']}
        print(data)
        things[thing_id] = data
        return data, 201

class ThingList(Resource):
    def get(self):
        return things

#    def post(self):
#        args = parser.parse_args()
#        thing_id = int(max(things.keys()).lstrip('id_')) + 1
#        thing_id = 'id_%i' % thing_id
#        things[thing_id] = {'data': args['data']}
#        return things[thing_id], 201


class IOTConfig(Resource):
    def get(self, id):
        abort_if_config_doesnt_exist(id)
        return configs[id]


api.add_resource(ThingList, '/data')
api.add_resource(Thing, '/data/<thing_id>')
api.add_resource(IOTConfig, '/config/<id>')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=2000)


#curl http://192.168.2.1:2000/data/70a1b200 -d '{"data":124}' -X POST -v --header "Content-Type: application/json" 
#curl http://192.168.2.1:2000/data -X GET -v

