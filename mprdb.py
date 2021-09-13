import argparse
import sys
import os


def key_management():
    # Key management
    # argv = key
    ## -i --init
    arg_init = args.init
    iinfo = 'TBD'
    return info


def register():
    # Register argv
    # argv = reg
    # -n --name
    # -p --passphrase
    arg_name = args.name
    arg_passphrase = args.passphrase
    
    if arg_name=='None' :
        info = 'Missing parameter : --name'
        return info
    else:
        command = 'python3 register.py -n '+arg_name
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)


def new_submit():
    # New submits
    # argv = new
    # -n --name
    # -r --reason
    # -s --score
    # -p --passphrase
    arg_name = args.name
    arg_reason = args.reason
    arg_score = args.score
    arg_passphrase = args.passphrase
    
    if arg_name=='None' or arg_reason == 'None' or arg_score == 'None':
        info = 'Missing parameter : --name or --reason or --score'
        return info
    else:
        command = 'python3 new_submit.py -n '+arg_name+' -r '+arg_reason+' -s '+arg_score
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)

def delete_submit():
    # Delete submits
    # argv = del
    # -u --uuid
    # -r --reason
    # -p --passphrase
    arg_uuid = args.uuid
    arg_reason = args.reason
    arg_passphrase = args.passphrase
    if arg_uuid=='None' or arg_reason == 'None':
        info = 'Missing parameter : --reason or --uuid'
        return info
    else:
        command = 'python3 delete_submit.py -u '+arg_uuid+' -r '+arg_reason
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)


def delete_server():
    # Delete server
    # argv = shut
    # -r --reason
    # -p --passphrase
    arg_reason = args.reason
    arg_passphrase = args.passphrase
    if arg_reason == 'None':
        info = 'Missing parameter : --reason'
        return info
    else:
        command = 'python3 delete_server.py'+' -r '+arg_reason
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)


def list_all_servers():
    # List all servers
    # argv = list
    # -m --max
    arg_max = str(args.max)
    command = 'python3 get_all_servers.py'
    if arg_max != '':
        command = command + ' -m '+arg_max
    os.system(command)


def get_submit_detail():
    # Get submit detail
    # argv = detail
    # -u --uuid
    arg_uuid = args.uuid
    if arg_uuid == 'None':
        info = 'Missing parameter : --uuid.'
        return info
    else:
        command = 'python3 get_submit_detail.py'+' -u '+arg_uuid
        os.system(command)

def get_submit_from_server():
    # Get submit from server
    # argv = listfrom
    # -u --uuid
    arg_uuid = args.uuid
    if arg_uuid == 'None':
        info = 'Missing parameter : --uuid.'
        return info
    else:
        command = 'python3 get_submit_from_other_servers.py'+' -u '+arg_uuid
        os.system(command)


def help_info():
    print('')
    return info

def update():
    os.system('python3 update.py')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="main")

    # register sub keys
    parser.add_argument('-u', '--uuid', default='None')
    parser.add_argument('-m', '--max', default='45')
    parser.add_argument('-n', '--name', default='None')
    parser.add_argument('-r', '--reason', default='None')
    parser.add_argument('-s', '--score', default='None')
    parser.add_argument('-p', '--passphrase', default='')
    parser.add_argument('-i', '--init', default='None')

    # register main keys
    parser.add_argument('--key', action='store_true', default=False)
    parser.add_argument('--reg', action='store_true', default=False)
    parser.add_argument('--new', action='store_true', default=False)
    parser.add_argument('--delete', action='store_true', default=False)
    parser.add_argument('--shut', action='store_true', default=False)
    parser.add_argument('--list', action='store_true', default=False)
    parser.add_argument('--detail', action='store_true', default=False)
    parser.add_argument('--listfrom', action='store_true', default=False)
    parser.add_argument('--update', action='store_true', default=False)

    args = parser.parse_args()

    if args.key == True:
        info = key_management()
        print(info)
    elif args.reg == True:
        info = register()
        print(info)
    elif args.new == True:
        info = new_submit()
        print(info)
    elif args.delete == True:
        info = delete_submit()
        print(info)
    elif args.shut == True:
        info = delete_server()
        print(info)
    elif args.list == True:
        list_all_servers()
    elif args.detail == True:
        info = get_submit_detail()
        print(info)
    elif args.listfrom == True:
        info = get_submit_from_server()
        print(info)
    elif args.update == True:
        update()
    else:
        print('Invalid parameter.')
        help_info()
