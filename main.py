import cmd
import json
import re
import requests
from collections import defaultdict

#ВФЫВФЫв укуксукс ацукаука https://dzen.ru/ https://www.facebook.com

class Cli(cmd.Cmd):

    def __init__(self, lens):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Hello\n for help enter 'help'"
        self.lens = lens
        if type(lens) == str:
            self.lens = lens.split(' ')
        self.methods = {'GET': requests.get,
                        "POST": requests.post,
                        "HEAD": requests.head,
                        "PUT": requests.put,
                        "DELETE": requests.delete,
                        "OPTIONS": requests.options,
                        "PATCH": requests.patch
                        }
        self.links = []

    def do_count_all(self, args):
        """count input lines"""
        count = len(self.lens)
        print(count)
        return count

    def do_check(self, args):
        """check string for reference"""
        response_urls = defaultdict(dict)
        for url in self.lens:
            if re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
                for key, value in self.methods.items():
                    response = value(url)
                    if response.status_code != 405:
                        response_urls[url][key] = response.status_code
            else:
                print(f"String {url} is't a link")
        print(json.dumps(response_urls, sort_keys=True, indent=4))
        return json.dumps(response_urls, sort_keys=True, indent=4)

    def do_reInput(self, args):
        """overwriting a list of strings"""
        self.lens = input("Input links: ").split(' ')
        return self.lens

    def do_count_links(self, args):
        """count links in input data"""
        for url in self.lens:
            if re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
                self.links.append(url)
        print(len(self.links))
        return len(self.links)

    def default(self, line):
        print("command not found")


if __name__ == "__main__":
    cli = Cli(lens=input("Input links (example: https://www.facebook.com https://dzen.ru https://yandex.ru : "))
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("exit...")
