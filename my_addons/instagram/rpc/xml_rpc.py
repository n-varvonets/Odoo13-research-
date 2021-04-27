# cd <to dir of file>
# python3.6 -m xml_rpc

url = "http://localhost:8069"
db = 'alex'
username = 'nickolay.varvonets@1000geeks.com'
password = 'QQQqqq111'

import xmlrpc.client

"""Logging in"""
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
print("details...", version)
# >>> details... {'server_version': '13.0', 'server_version_info': [13, 0, 0, 'final', 0, ''], 'server_serie': '13.0', 'protocol_version': 1}

"""make auth-tion"""
uid = common.authenticate(db, username, password, {})
print("UID", uid)


"""Calling methods""" 

"""List records"""
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))  # indicate object of db
partner_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])  # fetch the data from db table    [[['is_company', '=', True]]]) - also can add domain
print("take data from partner table....",partner_ids)
# >>> take data from partner table.... [14, 26, 33, 27, 10, 35, 18, 19, 11, 20, 22, 31, 23, 15, 34, 12, 21, 25, 37, 24, 36, 30, 38, 13, 29, 28, 9, 17, 32, 16, 1, 39, 40, 8, 7, 3]

"""Pagination(нумерация, сколько записей вывсести за один раз)"""
partner_pag_ids = models.execute_kw(db, uid, password, 'res.partner', 'search',[[]],  {'offset': 10, 'limit': 3})
print("partner is ....", partner_pag_ids)  # >>> partner is .... [22, 31, 23, 15, 34]

"""Read records"""
# ранее где мы получили айдишники партнеров с помощью partner = models.execute_kw - передаем их 
all_patrner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner_ids])  # это вывзовит все поля, которые не особо нужны, поэтому можно указать какие именно мы хотим получить записи:
specified_partner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner_pag_ids], {'fields': ['id', 'name']})
# print('specified_partner_rec is ....', specified_partner_rec)
# >>> specified_partner_rec is .... [{'id': 14, 'name': 'Azure Interior'}, {'id': 26, 'name': 'Brandon Freeman'}, ...
for partner in specified_partner_rec: 
	print(partner)

"""Search and read"""
search_read = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 3})
for partner in search_read:
	print('s&r',partner)

"""Create records"""
# к примеру в таблице res.partner создадим новую запись указа все required fields
new_contact = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Contact", 'mobile': "1234", 'website': "Test"}])
print('New contact ID....', new_contact)


"""Update records"""
dont_know = models.execute_kw(db, uid, password, 'res.partner', 'write', [[partner_ids], {
    'name': "Newer partner"
}])
# get record name after having changed it
dont_know_o = models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[partner_ids]])
print('dont_know', dont_know, dont_know_o)








