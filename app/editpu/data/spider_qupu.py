#coding=utf-8
import requests
import sys
import json
from datetime import datetime
from bs4 import BeautifulSoup
from operatedb import insert_qupu_todb,check_qupu_todb
reload(sys)
sys.setdefaultencoding('utf-8')

def get_page_datas(page_num):
    page_url = "https://www.acgmuse.com/page/%s/"%page_num
    respons = requests.get(page_url)
    soup = BeautifulSoup(respons.text,"html.parser")
    div_page = soup.find('div',{"class","col-mb-12 col-8"})

    chapter_div_list = div_page.find_all('div',{"class","card-title"})
    page_datas_list = []
    for key in chapter_div_list:
        page_datas_list.append(key.find('a')['href'])

    return page_datas_list


def get_qupu_data(url):
    #url = "https://www.acgmuse.com/archives/1915.html"
    print url
    respons = requests.get(url)
    soup = BeautifulSoup(respons.text,"html.parser")
    lists = soup.find('div',{'class':"music-score"})
    qupu_name = soup.find('h3',{'class':'post-title'}).get_text()
    introduce_list = soup.find('div',{'class':"post-content"})
    check_str = ""
    # 收集者 扒谱人 来源 歌手 所属专辑
    carrier = ""
    provider = ""
    provider_url = ""
    singer = ""
    anime = ""
    if introduce_list.find('p')!=None:
        for key in  introduce_list.find('p'):
            if type(key).__name__ == "NavigableString":
                if key.string.find("收集")!=-1:
                    carrier = key.string
                if key.string.find("供谱")!=-1:
                    provider = key.string
                if key.string.find("来源")!=-1:
                    provider_url = key.string
                if key.string.find("歌手")!=-1:
                    singer = key.string
                if key.string.find("所属专辑")!=-1:
                    anime = key.string
    introduce_dict = {"carrier":carrier,"provider":provider,"provider_url":provider_url,"singer":singer,"anime":anime}
    temp_str = ""
    if lists==None:
        print "非正常格式"
        if introduce_list.find('p')!=None:
            for key in introduce_list.find_all('p'):
                if key.name  == "p":
                    temp_str = temp_str + key.get_text() + '\n'

            temp_str = (temp_str.replace(u"\u2003"," "))
            # data = json.dumps(kkk, ensure_ascii=False)
            # print  data
            qupu_id = url.split('/')[-1].replace('.html',"")
            return qupu_id,qupu_name,url,introduce_dict,temp_str
    for key in lists:
        if type(key).__name__ == "Tag":
            if key.name == "br":
                temp_str = temp_str + '\n'
            if key.name == "sup":
                temp_str = temp_str + key.get_text()
        if type(key).__name__ == "NavigableString":
            if key.string!=None:
                temp_str = temp_str + key.string

    temp_str = (temp_str.replace(u"\u2003"," "))
    qupu_id = url.split('/')[-1].replace('.html',"")
    return qupu_id,qupu_name,url,introduce_dict,temp_str


#get_qupu_data("https://www.acgmuse.com/archives/797.html")

# carrier = ""
# provider = ""
# provider_url = ""
# singer = ""
# anime = ""

#id,name,url,provider,provider_url,anime,score_text,opreat_type,old_url
for num in range(1,379):
    page_datas_list = get_page_datas(num)
    for key in page_datas_list:
        try:
            qupu_id,qupu_name,url,introduce_dict,score_text = get_qupu_data(key)
            if check_qupu_todb(qupu_id):
                continue
            now_time = datetime.now()
            insert_list = [qupu_id,now_time,qupu_name,url,introduce_dict['provider'],introduce_dict['provider_url'],introduce_dict['anime'],score_text,0,]
            insert_qupu_todb(insert_list)
        except:
            # 获取最后更新时间
            with open("log.txt",'a+') as f:
                f.writelines(key)
            continue

