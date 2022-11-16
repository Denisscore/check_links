import gevent.monkey
gevent.monkey.patch_all()
import cmd
import json
import re
import requests
from collections import defaultdict


METHODS_HTTP = {"GET": requests.get,
                "POST": requests.post,
                "HEAD": requests.head,
                "PUT": requests.put,
                "DELETE": requests.delete,
                "OPTIONS": requests.options,
                "PATCH": requests.patch
                }


def check_lines(lines):
    links = []
    strings = []
    links.clear()
    for line in lines:
        if re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line):
            links.append(line)
        else:
            strings.append(line)
    return links, strings


def send_request(url, methods=None):
    if methods is None:
        methods = METHODS_HTTP
    response_urls = defaultdict(dict)
    for key, value in methods.items():
        response = value(url)
        if response.status_code != 405:
            response_urls[url][key] = response.status_code
    print(json.dumps(response_urls, sort_keys=True, indent=4))
    return json.dumps(response_urls, sort_keys=True, indent=4)


class Cli(cmd.Cmd):

    def __init__(self, lens):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Hello\n for help enter 'help'"
        self.lens = lens
        if type(lens) == str:
            self.lens = lens.split(' ')
        self.links, self.strings = check_lines(self.lens)


    def do_check(self, args):
        """check string for reference"""
        for string in self.strings:
            print(f"String {string} is't a link")
        for link in self.links:
            print(f"String {link} is a link")

    def do_send_request(self, args):
        """send comand for url"""
        jobs = [gevent.spawn(send_request, _url) for _url in self.links]
        gevent.wait(jobs)

    def do_count_all(self, args):
        """count input lines"""
        count = len(self.lens)
        print(count)
        return count

    def do_count_links(self, args):
        """count links in input data"""
        count = len(self.links)
        print(count)
        return count

    def default(self, line):
        print("command not found")


if __name__ == "__main__":
    cli = Cli(lens=input("Input links (example: https://www.facebook.com https://dzen.ru https://yandex.ru): "))
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("exit...")
