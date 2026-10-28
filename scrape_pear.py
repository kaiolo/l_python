# import json
# import requests
# import time
# url="https://www.pearvideo.com/video_1807991"
# srcurl="https://video.pearvideo.com/mp4/short/20261028/1793174374337-16083910-hd.mp4"

# systemTime=int(time.time())
# srcurl=srcurl.replace("1793174374337",str(systemTime))

# req=requests.get(srcurl ,headers={"referer":"https://www.pearvideo.com/video_1807991",
#                                   "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0"})
# print(req.json())     
import os

import requests
import random

cont_id = "1807991"
headers = {
    "Referer": f"https://www.pearvideo.com/video_{cont_id}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0"
}

# 1. 请求接口拿到json
mrd = random.random()
api_url = f"https://www.pearvideo.com/videoStatus.jsp?contId={cont_id}&mrd={mrd}"
resp = requests.get(api_url, headers=headers)
res_json = resp.json()

# 2. 替换得到真实mp4链接
fake_src = res_json["videoInfo"]["videos"]["srcUrl"]
sys_time = res_json["systemTime"]
real_url = fake_src.replace(sys_time, f"cont-{cont_id}")
print("真实视频地址：", real_url)

# 3. 下载视频（二进制，不要 .json()！）
video_resp = requests.get(real_url, headers=headers)
with open("pear.mp4", "ab") as f:
    f.write(video_resp.content)
print("下载完成")
print("本次拿到字节数：", len(video_resp.content))
print("文件现在大小：", os.path.getsize("pear.mp4"))