"""
Spyder Editor
Name: Adit Venkataraman
"""

import os
from starbase import Connection

con = Connection(port = 20550)


t = con.table('enron_venkat')
t.drop()
t.create('user', 'address', 'datetime', 'body')


row_ind = 0
user_names = os.listdir('/home/public/course/enron/') #extract subfolder names as list of user_names
for user in user_names:
    user_path = os.path.join('/home/public/course/enron/', user) 
    emails = os.listdir(user_path) #extract subfile names as list of email names within each users' folders
    
    for email in emails:
        email_path = os.path.join(user_path, email)
        with open(email_path) as f:
            lines = f.readlines()

       
        
        week_day = lines[1][:-1].split(' ')[1]
        day = lines[1][:-1].split(' ')[2]
        month = lines[1][:-1].split(' ')[3]
        year = lines[1][:-1].split(' ')[4]
        time = lines[1][:-1].split(' ')[5]

        address_from = lines[2][:-1].split(' ')[1]
        address_to = lines[3][:-1].split(' ')[1]

        body = False
        for ind, line in enumerate(lines):
            if line[:10] == 'X-FileName':
                body = True
                starting_line= ind
                break

        content = ''.join(lines[starting_line+1:])

        data = {
            'user': {'name': user},
            'address': {'from': address_from, 'to': address_to},
            'datetime': {'week_day': week_day, 'day': day, 'month': month, 'year': year, 'time': time},
            'body': {'body': content}
        }
        t.insert('row' + str(row_ind), data)
        row_ind += 1


query_user = 'mCarson'
content = ''
for row in range(row_ind):
    record = t.fetch('row' + str(row), ['user', 'body'])
    if record['user']['name'] == query_user:
        content += record['body']['body']

with open('5_3.txt', 'w') as f:
    f.write(content)


query_month = 'Oct'
content = ''
for row in range(row_ind):
    record = t.fetch('row' + str(row), ['body', 'datetime'])
    if record['datetime']['month'] == query_month:
        content += record['body']['body']

with open('5_4.txt', 'w') as f:
    f.write(content)



query_user = 'mCarson'
query_month = 'Oct'
content = ''
for row in range(row_ind):
    record = t.fetch('row' + str(row), ['user', 'body', 'datetime'])
    if record['user']['name'] == query_user and record['datetime']['month'] == query_month:
        content += record['body']['body']

with open('5_5.txt', 'w') as f:
    f.write(content)
