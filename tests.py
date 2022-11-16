from main import Cli, send_request, check_lines, METHODS_HTTP
import re
import json



def test_count_all():
    links = ['укукrtrкс', 'а32ed4//tert.com', 'https://dzen.ru/', 'https://www.facebook.com', 'https:/google.com']
    object_count = Cli(lens=links).do_count_all(links)
    assert object_count == len(links)


def test_count_links():
    links = ['укукrtrкс', 'а32ed4//tert.com', 'https://dzen.ru/', 'https://www.facebook.com', 'https:/google.com']
    links_test = [link for link in links if re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link)]
    object_count = Cli(lens=links).do_count_links(links)
    assert object_count == len(links_test)


def test_check():
    lines = ['укукrtrкс', 'https://www.facebook.com', 'это строка']
    links, string = check_lines(lines)
    assert len(links) == 1 and len(string) == 2

def test_send_request():
    lines = 'https://www.facebook.com'
    response = json.loads(send_request(lines))
    for key in METHODS_HTTP.keys():
        assert response['https://www.facebook.com'][f"{key}"] == 200
