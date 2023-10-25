import os
import json
import requests
from dateutil import parser

def format_date(date_str):
    # 解析日期字符串为datetime对象
    date = parser.parse(date_str)

    # 将datetime对象转换为年月日格式字符串
    return date.strftime("%Y.%m.%d")

def save_data_as_json(data, identifier, output_dir):
    # 将数据保存为JSON文件，并以identifier值作为文件名
    output_file = os.path.join(output_dir, f"{identifier}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_data_and_save(device_name, input_dir, output_dir):
    # 读取特定设备的JSON文件
    input_file = os.path.join(input_dir, f"{device_name}.json")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取每个固件的所需数据并创建一个列表
    firmware_data_list = []
    for item in data:
        firmware_data = {
            "id": item.get("id"),
            "identifier": item.get("identifier"),
            "name": item.get("name"),
            "release_date": item.get("release_date")
        }
        firmware_data_list.append(firmware_data)

    # 将提取的数据保存到对应的type.json文件
    output_file = os.path.join(output_dir, f"{device_name}type.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(firmware_data_list, f, ensure_ascii=False, indent=2)

    print(f"已保存JSON文件: {output_file}")

def main():
    devices = {
        "device1": "iPhone",
        "device2": "iPad",
        "device3": "Mac"
    }

    # 定义保存文件的目录
    output_dir = "/www/wwwroot/lanrenwanji.top/auto/output/ipsw"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for device_key, device_name in devices.items():
        device_url = f"https://betahub.cn/api/apple/devices/{device_name}"
        response = requests.get(device_url)
        devices_data = response.json()

        all_data = []

        for device in devices_data:
            identifier = device.get("identifier")

            url1 = f"https://betahub.cn/api/apple/firmwares/{identifier}?type=1"
            url2 = f"https://betahub.cn/api/apple/firmwares/{identifier}?type=2"

            response1 = requests.get(url1)
            data1 = response1.json()

            filtered_data1 = {
                "id": data1.get("id"),
                "name": data1.get("name"),
                "identifier": data1.get("identifier"),
                "release_date": data1.get("release_date"),
                "firmwares": []
            }

            for firmware1 in data1.get("firmwares", []):
                filtered_firmware1 = {
                    "id": firmware1.get("id"),
                    "version": "iOS " + firmware1.get("version") if device_name == "iPhone" else
                               "iPadOS " + firmware1.get("version") if device_name == "iPad" else
                               "MacOS " + firmware1.get("version") if device_name == "Mac" else firmware1.get("version"),
                    "build_id": firmware1.get("build_id"),
                    "size": f"{round(firmware1.get('size') / 1073741824, 2):.2f}GB",
                    "url": firmware1.get("url"),
                    "created_at": firmware1.get("created_at"),
                    "type": firmware1.get("type"),
                    "signing": firmware1.get("signing")
                }
                filtered_data1["firmwares"].append(filtered_firmware1)

            if url2:
                response2 = requests.get(url2)
                data2 = response2.json()

                filtered_data2 = {
                    "id": data2.get("id"),
                    "name": data2.get("name"),
                    "identifier": data2.get("identifier"),
                    "release_date": data2.get("release_date"),
                    "firmwares": []
                }

                for firmware2 in data2.get("firmwares", []):
                    filtered_firmware2 = {
                        "id": firmware2.get("id"),
                        "version": firmware2.get("version"),
                        "build_id": firmware2.get("build_id"),
                        "size": f"{round(firmware2.get('size') / 1073741824, 2):.2f}GB",
                        "url": firmware2.get("url"),
                        "created_at": firmware2.get("created_at"),
                        "type": firmware2.get("type"),
                        "signing": firmware2.get("signing")
                    }
                    filtered_data2["firmwares"].append(filtered_firmware2)

                if filtered_data1.get("name") == filtered_data2.get("name"):
                    filtered_data1["firmwares"].extend(filtered_data2["firmwares"])

            all_data.append(filtered_data1)

        # 将每个固件数据中的created_at和release_date转换为年月日格式   
        for data in all_data:
            data["release_date"] = format_date(data["release_date"])
            for firmware in data["firmwares"]:
                firmware["created_at"] = format_date(firmware["created_at"])

        # 输出为JSON格式并保存为相应设备名称的文件
        output_json = json.dumps(all_data, ensure_ascii=False)
        filename = os.path.join(output_dir, f"{device_name}.json")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(output_json)

        print(f"已保存JSON文件: {filename}")

        # 读取和处理每个JSON文件
        data = read_json_file(filename)
        for item in data:
            identifier = item.get('identifier', '')
            if identifier:
                save_data_as_json(item, identifier, output_dir)
            else:
                print(f"Warning: {filename}中的某个项缺少'identifier'字段。")

        # 提取id、identifier、name、release_date并保存到相应的type.json文件
        extract_data_and_save(device_name, output_dir, output_dir)

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    main()
