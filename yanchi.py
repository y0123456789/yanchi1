import json
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse
import os


# 获取json文件
url = "https://y0123456789.github.io/check-pallas/minified-v3.json"
response = requests.get(url).json()

# 获取mobileconfig模板文件
template_url = "https://dhinakg.github.io/check-pallas/template.mobileconfig"
template = requests.get(template_url).text

# 循环修改模板文件并保存mobileconfig文件
for minor_version in response["minorVersions"]:
    # 获取天数差
    if minor_version["date"]:
        delta = datetime.now(timezone.utc) - datetime.fromisoformat(minor_version["date"].replace("Z", "+00:00"))
        days = delta.days
    else:
        days = 0

    # 修改mobileconfig文件
    mobileconfig = template.replace("{DELAYPERIOD}", str(minor_version["delay"]))

    # 保存mobileconfig文件
    filename = f"{minor_version['name']} —剩余{days}天.mobileconfig"
    with open(filename, "w") as f:
        f.write(mobileconfig)

    # 添加mobileconfig文件的url到json文件中
    url = urlparse(template_url)._replace(path=filename).geturl()
    minor_version["url"] = url

# 保存修改后的json文件
with open("yanchi.json", "w") as f:
    json.dump(response, f)

print("生成yanchi.json文件成功！")
