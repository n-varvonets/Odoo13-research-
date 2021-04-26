# python3.6 -m json_rpc

import json
import random
import urllib.request


HOST = 'localhost'
PORT = 8069
DB = 'alex'
USER = 'nickolay.varvonets@1000geeks.com'
PASS = 'QQQqqq111 '


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)
print(url, uid)  # http://localhost:8069/jsonrpc False

"""# create a new note
args = {
    'memo': 'Test not from json rpc',
}  # memo is required field for creating new record
note_id = call(url, "object", "execute", DB, uid, PASS, 'note.note', 'create',args)  # note.note  модуль в который будем передавать новую запись методом криэйт и пердавая в args  наш словарь

print('created nir id ....', note_id)"""
