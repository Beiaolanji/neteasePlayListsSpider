# 爬取网易云歌单
import re
from selenium import webdriver
from .models import *
from selenium.webdriver.chrome.options import Options


# 传递前端输入的key_word,并搜索key_word对应的歌单
def search(key_word):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage') #Linux系统下的可选项
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)
    url = "https://music.163.com/#/search/m/?type=1000&s=" + key_word
    browser.get(url=url)
    browser.switch_to.frame(browser.find_element_by_id("g_iframe"))
    url = browser.find_element_by_class_name('ttc').find_element_by_tag_name('a').get_attribute('href')  # 取第一个匹配的歌单
    get_list(url, browser)
    browser.quit()


# 爬取歌单
def get_list(url, browser):
    # url = "https://music.163.com/playlist?id=2492426291"

    # browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
    browser.get(url=url)
    browser.switch_to.frame(browser.find_element_by_id("g_iframe"))
    list_lis = browser.find_element_by_id("song-list-pre-cache").find_element_by_tag_name(
        "tbody").find_elements_by_tag_name("tr")

    list_ensure_song = []
    for index, i in enumerate(list_lis):
        url = re.search("\?id=[0-9]{0,11}", i.find_element_by_tag_name("a").get_attribute("href")).group()
        url = "https://music.163.com/song/media/outer/url" + url + ".mp3"
        song_name = i.find_element_by_tag_name("b").get_attribute("title")
        song_time = i.find_element_by_class_name("u-dur").text
        list_temp = i.find_elements_by_tag_name("td")
        singer_name = list_temp[-2].find_element_by_tag_name("span").get_attribute("title")
        album_name = re.sub("\\xa0", " ", list_temp[-1].find_element_by_tag_name("a").get_attribute("title"))
        if not Singer.objects.filter(name=singer_name):
            sg = Singer(name=singer_name)
            sg.save()

        if not Album.objects.filter(name=album_name):
            al = Album(name=album_name)
            al.save()

        if not PlayList.objects.filter(name=song_name):
            pl = PlayList(name=song_name, url=url, time=song_time, singer=Singer.objects.get(name=singer_name),
                          album=Album.objects.get(name=album_name))
            # album_id = Album.objects.get(name=album_name).id
            pl.save()
            list_ensure_song.append(pl)
        else:
            PlayList.objects.filter(name=song_name).update(name=song_name, url=url, time=song_time,
                                                           singer=Singer.objects.get(name=singer_name),
                                                           album=Album.objects.get(name=album_name))
        print("*" * 20 + "已处理第%d个歌曲" % (index + 1) + "*" * 20)

    # 爬取评论数
    for index, i in enumerate(list_ensure_song):
        try:
            url = re.search("\?id=[0-9]{0,11}", i.url).group()
            url = "https://music.163.com/song" + url
            browser.get(url=url)
            browser.switch_to.frame(browser.find_element_by_id("g_iframe"))
            comment = browser.find_element_by_class_name('sub').find_element_by_class_name('j-flag').text
            i.comment = comment
            i.save()
            print("*" * 20 + "正在加载第%d条评论数" % (index + 1) + "*" * 20)
        except:
            pass
    return True
