import json
from pathlib import Path
import requests
from datetime import datetime, timezone, timedelta
import pytz
from urllib.parse import urlparse
import os


# 获取json文件
url = "https://y0123456789.github.io/check-pallas/minified-v3.json"
response = requests.get(url).json()

# 提取更新时间保存为date文件
#date = response["_date"]
time_str = response["_date"]
# 将时间字符串转换为 datetime 对象
dt = datetime.fromisoformat(time_str)
# 设置 UTC 时区
utc_tz = pytz.timezone('UTC')
# 将 datetime 对象转换为 UTC 时间
utc_dt = utc_tz.normalize(dt.astimezone(utc_tz))
# 设置上海时区
sh_tz = pytz.timezone('Asia/Shanghai')
# 将 UTC 时间转换为上海时区时间
sh_dt = sh_tz.normalize(utc_dt.astimezone(sh_tz))
# 格式化输出上海时区时间
sh_dt_str = sh_dt.strftime('%Y-%m-%d %H:%M:%S')
# 将时间保存到 date.json 文件中
with open('date.json', 'w') as f:
    json.dump({'date': sh_dt_str}, f)

    

    
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
template_url = "https://raw.githubusercontent.com/y0123456789/yanchi1/main/template.mobileconfig"
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
            mobileconfig = template.replace("{DELAYPERIOD}", str(version["delay"])).replace("{days}",str(version["days"]))
            mobileconfig = mobileconfig.replace("{NAME}", str(version["name"]))

            # 保存mobileconfig文件
            #filename = f"./{version['name']}剩余{days}天.mobileconfig"
            filename = f"./{version['name']}.mobileconfig"
            with open(filename, "w") as f:
                f.write(mobileconfig)

            # 将json字符串解析成字典
            # 修改字典中的值
            #url = urlparse(template_url)._replace(path=filename).geturl()
            #url = f"https://y0123456789.github.io/yanchi1/{version['name']}剩余{days}天.mobileconfig"      
            url = f"https://y0123456789.github.io/yanchi1/{version['name']}.mobileconfig"
            version["url"] = url
            
     # 提取更新时间保存为date文件
for versions in response.values():
    for version in versions:
        # 检查版本对象是否为字典类型，并且包含'date'字段
        if isinstance(version, dict) and version.get('date') is not None:
            time_str = version['date']
            # 将时间字符串转换为 datetime 对象
            dt = datetime.fromisoformat(time_str)
            # 设置 UTC 时区
            utc_tz = pytz.timezone('UTC')
            # 将 datetime 对象转换为 UTC 时间
            utc_dt = utc_tz.normalize(dt.astimezone(utc_tz))
            # 设置上海时区
            sh_tz = pytz.timezone('Asia/Shanghai')
            # 将 UTC 时间转换为上海时区时间
            sh_dt = sh_tz.normalize(utc_dt.astimezone(sh_tz))
            # 格式化输出上海时区时间
            sh_dt_str = sh_dt.strftime('%Y-%m-%d %H:%M:%S')
            # 将转换后的时间赋值给 version 字典的 'zhdate' 键
            version["zhdate"] = sh_dt_str
            # 打印转换后的 response 对象
            print(json.dumps(response, ensure_ascii=False))

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
        converted_data.append({"type": type, "list": array})

    # 将转换后的数据写入新的文件
    with open("yanchilist.json", "w") as file:
        json.dump(converted_data, file)
    
print("生成文件成功！")
