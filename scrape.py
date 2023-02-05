import requests
from bs4 import BeautifulSoup
import time
import pprint
import operator



def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['voes'], reverse=True)


def create_custom_page_hn(links, subtext):
    hn = []
    count = 0
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].a['href']
        vote = subtext[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'votes': points, 'title': title, 'link': href})
                count += 1

    return hn, count


def create_custom_hn():
    webpage = 'https://news.ycombinator.com/?p={page_num}'  # browser page = 1, 2, 3 ...
    pg = 1
    page_accumulator = []
    items = 0
    while True:
        page_addr = webpage.format(page_num=pg)
        # print(page_addr)
        res = requests.get(page_addr)  # browser page = 1, 2, 3 ...
        if res.status_code != requests.codes.ok:
            if res.status_code != 503:  # not server issue
                raise res.status_code  # http_error

            print('sleep')  # give the server time to recover
            time.sleep(2.0)
            continue

        # Everything is good
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titleline')
        subtext = soup.select('.subtext')
        morelink = soup.select('.morelink')

        hn_page, item_count = create_custom_page_hn(links, subtext)

        if len(hn_page) == 0:
            print('Empty page')
        print(f"page scrape: {pg}, items: {item_count}")
        if item_count > 0:
            page_accumulator.extend(hn_page)
            items += item_count

        if len(morelink) == 0:  # Stop when the morelink element is empty
            print(f"last page: {pg}")
            break

        pg += 1
        if pg > 30:
            print("over page limit")
            break
        time.sleep(0.5)  # don't overload the server
        # end of loop

    return sort_stories_by_votes(page_accumulator), items


if __name__ == '__main__':
    hn_filtered, accepted_items = create_custom_hn()
    print(f'Items: {accepted_items}')
    pp = pprint.PrettyPrinter()
    pp.pprint(hn_filtered)
    # print(hn_filtered)
    print(f'Items: {accepted_items}')
    print('done')
