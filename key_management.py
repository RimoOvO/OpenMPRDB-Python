# -- coding: utf-8 --
import gnupg
import pandas as pd
import configparser
import os
import argparse

parser = argparse.ArgumentParser(description="key management")
parser.add_argument('-m','--mode', default='manual')
parser.add_argument('-n','--name', default='None')
parser.add_argument('-e','--email', default='None')
parser.add_argument('-p','--passphrase', default='')
parser.add_argument('-c','--choice', default='0')
parser.add_argument('-l','--list', action='store_true', default=False)
args = parser.parse_args()


if not os.path.exists('gnupg'):
    os.mkdir('gnupg')

conf = configparser.ConfigParser()
gpg = gnupg.GPG(gnupghome='./gnupg')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)


def key_list():
    public_keys = gpg.list_keys()
    private_keys = gpg.list_keys(True)

    print("public_keys:")
    df = pd.DataFrame(public_keys)
    df1 = df.loc[:, ['keyid', 'length', 'uids', 'trust', 'date', 'fingerprint']]
    print(df1)

    print("private_keys:")
    df = pd.DataFrame(private_keys)
    df1 = df.loc[:, ['keyid', 'length', 'uids', 'trust', 'date', 'fingerprint']]
    print(df1)
    return


def key_generate():
    name_real = input("Input your name :")
    name_email = input("Input your email address :")

    while True:
        passphrase = input("Input passphrase :")
        if len(passphrase) == 0:
            print("Invalid input!")
        else:
            break
    print('Do you wan to save and auto fill your passphrase in the future?')
    choice = input('1 to save and auto fill,0 to skip this step.')
    if choice == '1':
        conf.read('mprdb.ini')
        conf.set('mprdb','save_passphrase','True')
        conf.set('mprdb','passphrase',passphrase)
        conf.write(open('mprdb.ini', 'w'))

    input_data = gpg.gen_key_input(name_email=name_email, passphrase=passphrase, name_real=name_real,
                                   key_length=2048)
    keyid = gpg.gen_key(input_data)
    key = str(keyid)  # key or keyid is its fingerprint
    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True, passphrase=passphrase)

    with open('public_key.asc', 'w+') as f:
        f.write(ascii_armored_public_keys)
    with open('private_key.asc', 'w+') as d:
        d.write(ascii_armored_private_keys)
    return


def key_import():
    key_data = open('key.asc').read()
    import_result = gpg.import_keys(key_data)
    print(import_result.results)
    return


def key_pub_export():
    key = input("Input the key id: ")
    try:
        ascii_armored_public_keys = gpg.export_keys(key)
    except:
        print("Invalid key id!")
        return
    with open('public_key.asc', 'w') as f:
        f.write(ascii_armored_public_keys)
    return


def key_pri_export():
    key = input("Input the key id: ")
    password = input("Input the key passphrase: ")
    try:
        ascii_armored_private_keys = gpg.export_keys(key, True, passphrase=password)
    except:
        print("Invalid key id or passphrase!")
        return
    with open('private_key.asc', 'w') as f:
        f.write(ascii_armored_private_keys)
    return


def sign_file():
    conf.read('mprdb.ini')
    keyid = conf.get('mprdb', 'ServerKeyId')
    with open('message.txt', 'rb') as f:
        gpg.sign_file(f, keyid=keyid, output='message.txt.asc')
    return


def verify_file():
    with open('message.txt.asc', 'rb') as f:
        verified = gpg.verify_file(f)
    if not verified:
        print("Signature could not be verified!")
    else:
        print("ok")
    return


def delete_key():
    keyfg = input("Input key fingerprint: ")
    passphrase = input("If it's a private key ,passphrase is required: ")
    print('Private key:')
    print(gpg.delete_keys(keyfg, True, passphrase=passphrase))
    print('Public key:')
    print(gpg.delete_keys(keyfg))

def key_generate_auto():
    name_real = args.name
    name_email = args.email
    passphrase = args.passphrase
    
    choice = args.choice
    if choice == '1':
        conf.read('mprdb.ini')
        conf.set('mprdb','save_passphrase','True')
        conf.set('mprdb','passphrase',passphrase)
        conf.write(open('mprdb.ini', 'w'))

    input_data = gpg.gen_key_input(name_email=name_email, passphrase=passphrase, name_real=name_real,
                                   key_length=2048)
    keyid = gpg.gen_key(input_data)
    key = str(keyid)  # key or keyid is its fingerprint
    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True, passphrase=passphrase)

    with open('public_key.asc', 'w+') as f:
        f.write(ascii_armored_public_keys)
    with open('private_key.asc', 'w+') as d:
        d.write(ascii_armored_private_keys)
    return

mode=args.mode
if mode == 'auto' :
    if args.name != 'None' and args.email != 'None' and args.passphrase != 'None':
        key_generate_auto()
        exit()
    else:
        print('Missing arguments.')
        exit()
elif mode == 'list':
    key_list()
    exit()

print("Usage:")
print("1. generate a key pair,command init")
print("2. list all keys,command list")
print("3. import keys,command im")
print("4. export public keys,command pub")
print("5. export private keys,command pri")
print("6. encrypt/sign a file,command en")
print("7. decrypt/verify a file,command de")
print("8. delete a key,command del")
print("9. to exit,command 0")

while True:
    command = input("Command: ")
    if command == "init":
        key_generate()
    elif command == "list":
        key_list()
    elif command == "im":
        key_import()
    elif command == "pub":
        key_pub_export()
    elif command == "pri":
        key_pri_export()
    elif command == "en":
        sign_file()
    elif command == "de":
        verify_file()
    elif command == "del":
        delete_key()
    elif command == "0":
        exit()
    else:
        print("Invalid input! Please re-enter.")
