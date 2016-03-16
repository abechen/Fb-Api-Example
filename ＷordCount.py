# encoding=utf8
import sys
import jieba
import requests
import json
import operator


def start():
    fb_token = ''
    year = '1388534400'
    req = requests.get('https://graph.facebook.com/me/posts?limit=100&since=' + year + '&access_token=' + fb_token)
    res = json.loads(req.text)  # response type is json

    corpus = []
    while 'paging' in res:
        for post in res['data']:
            if 'message' in post:  # get message
                corpus += jieba.cut(post['message'], cut_all=False, HMM=True)  # 分詞
        req = requests.get(res['paging']['next'])
        res = json.loads(req.text)

    dic = {}
    for word in corpus:
        if word not in dic:
            if len(word) > 1:
                dic[word] = 1
        else:
            dic[word] = dic[word] + 1

    # 排序資料，取前20筆
    dic_sorted = sorted(dic.items(), key = operator.itemgetter(1), reverse = True)
    dic_sorted = dic_sorted[1:20]
    for word in dic_sorted:
        print word[0], word[1]

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    start()
