import json
from pathlib import Path
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse
import os


# 获取json文件
url = "https://y0123456789.github.io/check-pallas/minified-v3.json"
response = requests.get(url).json()
# 删除指定的键值对
if "iOS (iPhone 14 series)" in response:
    response.pop("iOS (iPhone 14 series)")
if "iPadOS (October 2022 models)" in response:
    response.pop("iPadOS (October 2022 models)")
if "_date" in response:
    response.pop("_date")
if "iOS (all other devices supporting iOS 16)" in response:
    response["iOS (iPhone 8 - iPhone 14)"] = response.pop("iOS (all other devices supporting iOS 16)")
if "iOS Legacy v2 (device supporting up to iOS 15)" in response:
    response["iOS (iPhone 6s - iPhone 7)"] = response.pop("iOS Legacy v2 (device supporting up to iOS 15)")
if "iPadOS" in response:
    response["iPadOS (最高iPadOS 16)"] = response.pop("iPadOS")
if "iPadOS Legacy v2 (devices supporting up to iOS 15)" in response:
    response["iPadOS (最高iPadOS 15)"] = response.pop("iPadOS Legacy v2 (devices supporting up to iOS 15)")
if "macOS" in response:
    response["macOS"] = response.pop("macOS")
if "tvOS" in response:
    response["tvOS"] = response.pop("tvOS")

# 删除delay值为0和小于0的数据
for name, versions in response.items():
    for version in versions[:]:
        if isinstance(version, dict) and "delay" in version and version["delay"] <= 0:
            versions.remove(version)
# 如果数据为空，则删除对应的键值对
for name, versions in list(response.items()):
    if not versions:
        del response[name]
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
    #with Path("yanchi.json").open("w") as f:
         #json.dump(response, f)
        
    # 读取原始数据
    with open("yanchi.json", "r") as file:
       original_data = json.load(file)

    converted_data = []

    # 遍历原始数据，将每个类型与对应的数组转换为新的字典格式
    for type, array in original_data.items():
        converted_dict = {
        "type": type,
        "list": array
       }
       converted_data.append(converted_dict)

# 将转换后的数据写入新的文件
with open("converted_yanchi.json", "w") as file:
    json.dump(converted_data, file, indent=4)
    
print("生成文件成功！")
