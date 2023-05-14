import json
import requests
from io import BytesIO
from jinja2 import Template
from lxml import etree
from base64 import b64encode

# 获取 JSON 文件
json_url = "https://y0123456789.github.io/check-pallas/minified-v3.json"
response = requests.get(json_url).text
data = json.loads(response)

# 获取模板文件
template_url = "https://dhinakg.github.io/check-pallas/template.mobileconfig"
response = requests.get(template_url).text
template = Template(response)

# 填充模板并生成配置文件
xml_content = template.render(data=data)
xml_tree = etree.fromstring(xml_content.encode())
xml_string = etree.tostring(xml_tree, pretty_print=True)

# 保存为 mobileconfig 格式的文件
filename = f"{data['minor_version']['name']} —剩余{
