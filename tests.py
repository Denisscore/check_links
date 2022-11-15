from main import Cli
import re


def test_count_all():
    links = ['укукrtrкс', 'а32ed4//tert.com', 'https://dzen.ru/', 'https://www.facebook.com', 'https:/google.com']
    object_count = Cli(links).do_count_all(links)
    assert object_count == len(links)


def test_count_links():
    links = ['укукrtrкс', 'а32ed4//tert.com', 'https://dzen.ru/', 'https://www.facebook.com', 'https:/google.com']
    links_test = [link for link in links if re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link)]
    object_count = Cli(links).do_count_links(links)
    assert object_count == len(links_test)


def test_check():
    links = ['укукrtrкс', 'https://www.facebook.com']
    object_check = Cli(links).do_check(links)
    assert len(object_check) >= 0
