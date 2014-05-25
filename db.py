#!/usr/bin/python3.4

#############################################################################
#
#  Dictionnary DB managing script. Add/Del/Search definitions
#  Copyright (C) 2014 bertrand
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#############################################################################



###############
### Imports ###
import sys
import psycopg2 as PSQL
import textwrap as txtwrp



#####################
### Configuration ###
config = {
    'VERSION_MAJOR' : '0',
    'VERSION_MINOR' : '1',
    'dbname'        : 'bertrand',
    'user'          : 'bertrand'
}



#############
### USAGE ###
def usage():
    print("Tool to insert/remove entries in the dicotionnnary.")
    print("Version: " + config['VERSION_MAJOR'] + "." + config['VERSION_MINOR'])
    print("Usage: " + sys.argv[0] + " <command> <options>")
    print("")
    print("Commands:")
    print("  add     Add definition to dictionnary.")
    print("  del     Remove definition from dictionnary.")
    print("  help    Print general help or command specific help.")
    print("  search  Search definition in dictionnary.")
    print("")



###########
### ADD ###
def add():
    argc = len(sys.argv)
    if argc < 3:
        __help_cmd(sys.argv[1])
        return

    req = {
        'fields' : '',
        'name'   : '',
        'def'    : '',
        'url'    : ''
    }

    i=2
    while i < argc:
        if sys.argv[i] == "-d":
            i += 1
            req['def'] = sys.argv[i]
        elif sys.argv[i] == "-f":
            i += 1
            req['fields'] = sys.argv[i]
        elif sys.argv[i] == '-n':
            i += 1
            req['name'] = sys.argv[i]
        elif sys.argv[i] == "-u":
            i += 1
            req['url'] = sys.argv[i]
        else:
            print("Unknown option '" + sys.argv[i] + "'")
            __help_cmd(sys.argv[1])
            return
        i += 1

    if req['fields'] == '':
        print("Please specify fields with option '-f'.")
        __help_cmd(sys.argv[1])
        return
    elif req['name'] == '':
        print("Please specify fields with option '-f'.")
        __help_cmd(sys.argv[1])
        return
    elif req['def'] == '':
        print("Please specify definition with option '-d'.")
        __help_cmd(sys.argv[1])
        return

    conn = PSQL.connect("dbname=" + config['dbname'] + " user=" + config['user'])
    cur  = conn.cursor()
    req  = cur.mogrify("INSERT INTO dico (fields,name,def,url) VALUES (%s, %s, %s, %s)", 
            ("{" + req['fields'] + "}", req['name'], req['def'], req['url']))
    print(req)
    cur.execute(req)
    conn.commit()
    cur.close()
    conn.close()



###########
### DEL ###
def delete():
    try:
        defid = sys.argv[2]
    except IndexError:
        print("Missing argument.")
        __help_cmd(sys.argv[1])
        return

    conn = PSQL.connect("dbname=" + config['dbname'] + " user=" + config['user'])
    cur  = conn.cursor()
    req  = cur.mogrify("DELETE FROM dico WHERE id=%s", (defid,))
    print(req)
    cur.execute(req)
    conn.commit()
    cur.close()
    conn.close()



#####################
### HELP COMMANDS ###
def help_cmd():
    try:
        cmd = sys.argv[2]
    except:
        cmd = ''
    __help_cmd(cmd)



def __help_cmd(cmd):
    if cmd == '' :
        usage()

    elif cmd == "add" :
        print("Command '" + cmd + "': Add definition to dictionnary.")
        print("Usage: " + sys.argv[0] + " " + cmd + " <options>")
        print("")
        print("Options:")
        print("  -d <str>         Definition.")
        print("  -f <str,str,..>  List of fields.")
        print("  -n  <str>        Name of the entry")
        print("  -u  <url>        One url to a more complete definition.")
        print("")

    elif cmd == "del" :
        print("Command '" + cmd + "': Delete definition from dictionnary.")
        print("Usage: " + sys.argv[0] + " " + cmd + " <id>")
        print("")
        print("Param:")
        print("  id               ID of the definition to delete.")
        print("")

    elif cmd == "help" :
        print("Command '" + cmd + "': Print help.")
        print("Usage: " + sys.argv[0] + " " + cmd + " [command]")
        print("")
        print("Giving NO 'command' this will print the general help.")
        print("Giving 'command' this will print the command specific help. ")
        print("")

    elif cmd == "search" :
        print("Command '" + cmd + "': Search definition in dictionnary.")
        print("Usage: " + sys.argv[0] + " " + cmd + " <options>")
        print("")
        print("Options:")
        print("  -a                Print all definitions in the table.")
        print("  -f <str,str,...>  Print definitions matching the set of given fields.")
        print("  -i <id>           Print definition matching the given ID.")
        print("  -n <str>          Print definition mathing the given entry name.")
        print("")

    else:
        print("Unknown command: '" + cmd + "'")
        usage() 



##############
### SEARCH ###
def search():
    try:
        opt = sys.argv[2]
    except IndexError:
        __help_cmd(sys.argv[1])
        return
    else:
        if not opt in ('-a', '-f', '-i', '-n'):
            print("Unknown option '" + sys.argv[2] + "'")
            __help_cmd(sys.argv[1])
            return
    
    conn = PSQL.connect("dbname=" + config['dbname'] + " user=" + config['user'])
    cur  = conn.cursor()

    try:
        if opt == "-a":
            req = cur.mogrify("SELECT id,fields,name,def,url FROM dico")
        elif opt == "-f":
            optarg = sys.argv[3]
            req = __search_build_req_fields(optarg.split(','))
        elif opt == '-i':
            optarg = sys.argv[3]
            req = cur.mogrify("SELECT id,fields,name,def,url FROM dico WHERE id=%s", (optarg,))
        elif opt == "-n":
            optarg = sys.argv[3]
            req = cur.mogrify("SELECT id,fields,name,def,url FROM dico WHERE name=%s", (optarg,))
    except IndexError:
        print("Missing argument.")
        __help_cmd(sys.argv[1])
    else:
        print(req)
        cur.execute(req)
        print_rows(cur.fetchall())
        conn.commit()
    finally:
        cur.close()
        conn.close()



def __search_build_req_fields(fields):
    # How do you like your SQL injection?
    # I like mine crispy and with a python '+' ;)
    # http://initd.org/psycopg/docs/usage.html
    # http://xkcd.com/327/
    # That will do for now ...
    req = "SELECT id,fields,name,def,url FROM dico WHERE "
    req += "'" + fields[0] + "'=ANY(fields)"
    for f in fields[1:]:
        req += " OR '" + f + "'=ANY(fields)"
    return req



###################################
### PRINT PSQL REQUESTS RESULTS ###
def print_rows(rows):
    for row in rows:
        print("---------------------")
        print("ID     : ", row[0])
        __print_row_wrapped("FIELDS : ", row[1])
        __print_row_wrapped("NAME   : ", row[2])
        __print_row_wrapped("DEF    : ", row[3])
        __print_row_wrapped("URL    : ", row[4])
        print("")

def __print_row_wrapped(label, value):
    labellen = len(label)
    wrapped = txtwrp.wrap(value)

    print(label, wrapped[0])
    for i in range(1, len(wrapped)):
        print(' ' * labellen, wrapped[i])
        


############
### MAIN ###
commands = { 
    'add'    : add, 
    'del'    : delete,
    'help'   : help_cmd,
    'search' : search
}

try:
    cmd = sys.argv[1]
except KeyError:
    print("Unknown command: " + cmd)
    usage()
    sys.exit()
except IndexError:
    usage()
    sys.exit()
else:
    commands[cmd]()

