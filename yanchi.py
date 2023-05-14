import json
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse
import os

# 获取json文件
url = "https://y0123456789.github.io/check-pallas/minified-v3.json"
response = requests.get(url).json()

# 获取mobileconfig模板文件
template_url = "https://raw.githubusercontent.com/y0123456789/yanchi/main/template.mobileconfig"
template = requests.get(template_url).text

# 循环修改模板文件并保存mobileconfig文件
# 循环获取版本名称和更新时间
for name, versions in response.items():
    print(f"{name}:")
    for version in versions:
        if isinstance(version, dict) and version.get('date') is not None and version.get('delay') is not None and version.get('delay') >= 0:
            delta = datetime.now(timezone.utc) - datetime.fromisoformat(version["date"].replace("Z", "+00:00"))
            day = datetime.fromisoformat(version["date"].replace("Z", "+00:00")) - datetime.now(timezone.utc)
            days = day.days
            print(f"Name: {version['name']}, Date: {version['date']}, Delta: {delta}")

        else:
            days = 0


        # 修改mobileconfig文件
        if "delay" in version and version["delay"] >= 0:
            mobileconfig = template.replace("{DELAYPERIOD}", str(version["delay"]))
            mobileconfig = mobileconfig.replace("{NAME}", str(version["name"]))

            # 保存mobileconfig文件
            filename = f"./{version['name']} —剩余{days}天.mobileconfig"
            with open(filename, "w") as f:
                f.write(mobileconfig)

            # 将json字符串解析成字典
            # 修改字典中的值
            url = urlparse(template_url)._replace(path=filename).geturl()
            version["url"] = url

    # 将字典转换回json字符串并保存到文件中
    with open("yanchi.json", "w") as f:
        f.write(json.dumps(response))


print("生成yanchi.json文件成功！")
