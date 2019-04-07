from lxml import html
from datetime import date, datetime
import requests
import re
from sys import platform
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


def get_menu_from_html(html_tree):
    third_level_headers = html_tree.xpath('//h3')
    date_pp_menus = {}
    for h3_elem in third_level_headers:
        menu_date = get_date(h3_elem.text)
        if menu_date:
            list_menus = h3_elem.getparent().xpath('.//span[@class="name"]')
            list_menus_personnel_poelee = [x for x in list_menus if x.text == 'PERSONNEL Poêlée']
            menu_items = []
            for menu_pp in list_menus_personnel_poelee:
                menu_items.extend([x.text for x in menu_pp.getnext().xpath('.//li')])
            date_pp_menus[menu_date] = menu_items
    return date_pp_menus


def retrieve_html_from(ru_url_path):
    page = requests.get(ru_url_path)
    html_tree = html.fromstring(page.content)
    return html_tree


def check_for_canard(date_menus):
    canard_dates = {}
    for date_obj, menu in date_menus.items():
        canard_items = list(filter(lambda x: "Canard" in x or "canard" in x, menu))
        if canard_items:
            canard_dates[date_obj] = canard_items[0]
    return canard_dates


def main():
    if platform == "linux":
        locale.setlocale(locale.LC_ALL, "fr_FR.utf-8")
    else:
        locale.setlocale(locale.LC_ALL, "fr_FR")
    html_tree = retrieve_html_from(URL_RU)
    date_menus = get_menu_from_html(html_tree)
    canard_dates = check_for_canard(date_menus)
    if canard_dates:
        for date_obj, menu in canard_dates.items():
            print("Canard servi le {}: {}".format(date_obj.strftime("%A %d %B %Y"), menu))
    else:
        print("Pas de canard en vue")


if __name__ == "__main__":
    main()
