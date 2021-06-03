import requests
from urllib.parse import urlparse, parse_qs, parse_qsl

cookies = requests.cookies.RequestsCookieJar()


def getDyItemId(url):
    response = requests.get(url)
    cookies.update(response.cookies)
    redirectUrl = urlparse(response.url)
    path = redirectUrl.path.split("/")
    vp = path.index("video")
    itemId = path[vp + 1]
    return itemId


def getVideoUrl(itemId):
    url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + itemId
    response = requests.get(url)
    cookies.update(response.cookies)
    if response.status_code == 200:
        respJson = response.json()
        if respJson['status_code'] == 0:
            videoUrl = respJson['item_list'][0]['video']['play_addr']['url_list'][0]
            videoUrl = videoUrl.replace("playwm", "play")
            videoTitle = respJson['item_list'][0]['share_info']['share_title']
            print("请求 %s 成功" % url)
            print("视频地址为 %s " % videoUrl)
            return {"title": videoTitle, "url": videoUrl}


def saveVideo(videoUrl, path):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36"
    }
    r = requests.get(videoUrl, headers=headers)
    cookies.update(r.cookies)
    with open(path, "wb") as f:
        f.write(r.content)
        f.close()
        print("保存视频到 %s 成功" % path)


def run(url):
    itemId = getDyItemId(url=url)
    videoInfo = getVideoUrl(itemId)
    saveVideo(videoInfo['url'], "./video/" + videoInfo['title'] + '.mp4')


run("https://v.douyin.com/Jmq4Dcd/")
run("https://v.douyin.com/JmqpP72/")

# run("https://v.douyin.com/JPuaku5/")
# run("https://v.douyin.com/JPubYAj/")
# run("https://v.douyin.com/JPuHAgp/")

