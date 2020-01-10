from bs4 import BeautifulSoup
from os.path import curdir, abspath, join


CUR_DIR = abspath(curdir)
with open(join(CUR_DIR, 'newstyle.css'), 'r') as style_file:
    NEW_CSS = style_file.read()

def roster_parser(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    soup.style.string = NEW_CSS

    for li in soup.find_all('li', 'rootselection'):
        li.h4.wrap(soup.new_tag('summary'))
        li.wrap(soup.new_tag('li'))
        li.parent.attrs = {'class': 'rootselection'}
        li.wrap(soup.new_tag('details'))
        li.unwrap()
    return str(soup)
