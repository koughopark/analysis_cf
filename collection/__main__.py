import collection.crawler as cw


def proc(html):
    print("process.... :" + html)

def store(result):
    pass


result = cw.crawling(
    url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn',
    encoding='cp949',
    proc=proc,
    store=store)


# print("process.... :" + html) # proc, store를 crawler 안에다가 넣어줘서 처리한다.
