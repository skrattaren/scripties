#!/usr/bin/env python3

'''
Get lists of NBA uniform numbers from basketball-reference.com and print
unused ones within and since that year.
'''

import datetime
import urllib.error
import urllib.request

from bs4 import BeautifulSoup


UNI_NUMS_URL_TMPL = ('https://www.basketball-reference.com/leagues/'
                     'NBA_{}_numbers.html')
CSS_SEL = 'div#div_leaderboard div.data_grid_box table.no_columns caption'

CUR_YEAR = datetime.date.today().year


def get_all_nums():
    nums = set(str(n) for n in range(0, 100))
    nums.add('00')
    return nums


def get_used(year):
    try:
        with urllib.request.urlopen(UNI_NUMS_URL_TMPL.format(year)
                                    ) as response:
            html = response.read()
    except urllib.error.HTTPError:
        return None
    bshtml = BeautifulSoup(html, 'lxml')
    num_els = bshtml.select(CSS_SEL)
    return [e.text for e in num_els]


def main():
    year = CUR_YEAR
    unused_since = get_all_nums()
    while True:
        used_nums = get_used(year)
        if used_nums is None:
            break
        unused_nums = get_all_nums() - set(used_nums)
        print(" === {} ===".format(year))
        print(" Unused numbers this year")
        print(sorted(unused_nums))
        print(" Unused numbers *since* this year")
        unused_since = unused_since & unused_nums
        print(sorted(unused_since))
        if not unused_since:
            break
        year -= 1
        print()


if __name__ == '__main__':
    main()
