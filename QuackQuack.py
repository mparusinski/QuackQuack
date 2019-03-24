from lxml import html
from datetime import date, datetime
import requests
import re
import locale

URL_RU = 'http://www.crous-strasbourg.fr/restaurant/resto-u-illkirch/'
MENU_RE = re.compile(r'Menu du [a-z]+ ([0-9]+) ([a-z]+) ([0-9]+)')


def get_date(menu_string):
    date_match_obj = MENU_RE.match(menu_string)
    if date_match_obj:
        day = int(date_match_obj.group(1))
        month = datetime.strptime(date_match_obj.group(2), "%B").month
        year = int(date_match_obj.group(3))
        return date(year=year, month=month, day=day)


def retrieve_date_from_web(ru_url_path):
    page = requests.get(ru_url_path)
    tree = html.fromstring(page.content)
    third_level_headers = tree.xpath('//h3')
    date_pp_menus = {}
    for h3_elem in third_level_headers:
        menu_date = get_date(h3_elem.text)
        if menu_date:
            list_menus = h3_elem.getparent().xpath('.//span[@class="name"]')
            list_menus_personnel_poelee = [ x for x in list_menus if x.text == 'PERSONNEL Poêlée']
            menu_items = []
            for menu_pp in list_menus_personnel_poelee:
                menu_items.extend([ x.text for x in menu_pp.getnext().xpath('.//li')])
            date_pp_menus[menu_date] = menu_items
    return date_pp_menus


def main():
    locale.setlocale(locale.LC_ALL, "fr_FR")
    date_menus = retrieve_date_from_web(URL_RU)
    for date, menu in date_menus.items():
        print("{} :\t {}".format(date.strftime("%A %d %B %Y"), menu))


if __name__ == "__main__":
    main()
