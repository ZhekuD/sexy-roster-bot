from bs4 import BeautifulSoup
from os.path import curdir, abspath, join


CUR_DIR = abspath(curdir)
with open(join(CUR_DIR, 'newstyle.css'), 'r') as style_file:
    NEW_CSS = style_file.read()


def roster_style_parser(input_html, add_style=True):
    soup = BeautifulSoup(input_html, 'html.parser')
    if add_style:
        soup.style.string = NEW_CSS
    else:
        soup = soup.find_all("div", class_="battlescribe")[0]
    return str(soup)

def roster_body_parser(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    for li in soup.find_all('li', 'rootselection'):
        li.h4.wrap(soup.new_tag('summary'))
        li.wrap(soup.new_tag('li'))
        li.parent.attrs = {'class': 'rootselection'}
        li.wrap(soup.new_tag('details'))
        li.unwrap()
    return str(soup)
