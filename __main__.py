import urllib
from itertools import count
import pandas as pd

from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import collection.crawler as cw
from collection.data_dict import sido_dict, gungu_dict

RESULT_DIRECTORY = '__result__/crawling'


def proc(html):
    print("process.... :" + html)


def store(result):
    pass


# cw.crawling(
#     url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn',
#     encoding='cp949',
#     proc=proc,
#     store=store)
# print("process.... :" + html) # proc, store를 crawler 안에다가 넣어줘서 처리한다.

def crawling_pericana():
    results = []
    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html/?gu=&si=&page=%d' % page
        html = cw.crawling(url=url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')
        # print(page, len(tags_tr), sep=":")

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[3]
            # print(address.split())
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    # proc
    print(results)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


# kyochon 내가 지금 하고있는것
def crawling_kyochon():
    results = []

    for sido1 in range(1, 2):
        for sido2 in count(start=1):
            # if sido2 is not None:
            #     break

            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = cw.crawling(url=url)
            if html is None:
                break
            bs = BeautifulSoup(html, 'html.parser')

            tag_table = bs.find('ul', attrs={'class': 'list'})
            tag_li = tag_table.find('li')
            tag_dl = tag_li.findAll('dl')
            tag_dl1 = tag_li.find('dl')
            tag_dt = tag_dl1.find('dt')
            # tags_dd = tag_dl.findAll('dd')

            # 끝 검출
            if tag_dt is None:
                break

            for a in tag_dl:
                strings = list(a.strings)
                # print(strings)

                name = strings[1]
                address = strings[3].replace('\n', '').replace('\t', '')
                print(strings[3])
                # print(address.split())
                sidogu = address.split()[:2]

                results.append((name, address) + tuple(sidogu))

    # print(results)



        # proc
        # print(results)

        # store
        table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

        table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
        table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

        table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)






    #         if condition:
    #             break
    # pass


# nene
def proc_nene(xml):
    root = et.fromstring(xml)
    results = []

    elements_item = root.findall('item')
    for a in elements_item:
        name = a.findtext('aname1')
        sido = a.findtext('aname2')
        gungu = a.findtext('aname3')
        address = a.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results


def store_nene(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/nene_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)




# ***************************************************


if __name__ == '__main__':
    # pericana
    # crawling_pericana()

    # nene
    # cw.crawling(
    #     url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
    #         % (urllib.parse.quote("전체"), urllib.parse.quote("전체")),
    #     proc=proc_nene,
    #     store=store_nene
    # )

    # kyochon
    crawling_kyochon()