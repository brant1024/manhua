import requests
import time
import json
import os

# type=5&coType=10&pageNo=1&pageSize=30
##八月漫画采集程序
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'token': '443dfec54490168a31fc83369e862b15',
    'userId': '10130641'}


def down_content(url, head):
    content = requests.get(url, head)
    return content


# 排行榜
def get_pro():
    data = {
        'type': 5,
        'coType': 10,
        'pageNo': 1,
        'pageSize': 30,
        'state' : 1
    }

    #pageNo = 1 & pageSize = 10 & cartoonType = & state = 1 & price = & order = & coType = 10
    # 获取排行榜
    url = 'http://api.bawangmanhua.com/mobile/homePage/list-ranking'
    html = requests.post(url, data=data, headers=head)
    info = json.loads(html.text)
    content = []
    for i in info["cartoonList"]:
        content.append(i["id"])
    return content


# 获取作品集
def get_list(id):
    url1 = "http://api.bawangmanhua.com/mobile/cartoonCollection/detail"
    data1 = {
        'id': id
    }
    # id=1394
    html = requests.post(url1, data=data1, headers=head)
    info = json.loads(html.text)

    # print(info["cartoon"]["name"],  #作品名
    #       info["cartoon"]["chapCount"], #连载集数
    #       info["cartoon"]["probationChapterIds"],   #免费查看的id
    #       info["cartoon"]["chapterOfFree"],  #免费集数cnt
    #       info["cartoon"]["modStateStr"],   #连载状态
    #       info["cartoon"]["firstChapterId"],   #第一级ID
    #       )

    content = {}
    content["firstChapterId"] = info["cartoon"]["firstChapterId"]
    content["chapCount"] = info["cartoon"]["chapCount"]
    content["name"] = info["cartoon"]["name"]
    return content


# 获取明细图片
def get_picurl(id,name):
    url2 = "http://api.bawangmanhua.com/mobile/chapter/check-pay"
    data2 = {
        'id': id
    }
    html = requests.post(url2, data=data2, headers=head)
    info = json.loads(html.text)
    print(info)
    dic = {}
    dic["name"]=name
    dic["zjname"] = info["chapter"]["name"]  # 章节名
    dic["cartoonid"] = info["chapter"]["id"]  # 作品名编号
    dic["chapterchapterIndexStr"] = info["chapter"]["chapterchapterIndexStr"]  # 第几章
    dic["chapterid"] = info["chapter"]["id"]  # 章节ID
    for i in info["chapter"]["chapterPicVos"]:
        print(i["id"],
              i["picUrl"],
              i["pic"]
              )
        save_dir = 'd:/manhua/' + str(dic["name"]) + '/' + str(dic["chapterid"]) +str(dic["zjname"])+ '/'
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        with open(save_dir + str(i["id"]) + '.jpg', "wb") as code:
            code.write(down_content(i["picUrl"], head).content)

if __name__ == '__main__':
    list=get_pro()
    for i in list:
        dh=get_list(i)
        print(dh)
        try:
            for i in range(dh['firstChapterId'],dh['firstChapterId']+dh['chapCount']):
                print(i)
                get_picurl(i,dh["name"])
                time.sleep(0.1)
        except Exception as e:
            continue
        time.sleep(1)



