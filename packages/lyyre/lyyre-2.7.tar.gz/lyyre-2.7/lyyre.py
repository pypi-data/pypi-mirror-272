import re
import http.client
from lyylog import log
import json

def format_url_in_ocr_text_include_markdown_img(text,debug=False):
    if debug: print("enter format_ocr_text_include_markdown_img")
    url_pattern = r'!\s?\[\s?(?:screenshot)?\s?\]\s?\((http:?//.*\.(bmp)|(png)|(jpg))'

    # 在文本中查找所有匹配的网址
    matches = re.findall(url_pattern, text)
    if len(matches)>0:
        for match in matches:
            if debug: print(match)
            cleaned_url = re.sub(r'\s+', '', match[0])
            if debug: print(cleaned_url)
            return cleaned_url
    else:
        return text
    
def get_to_ocr_image_pdf_url(text,debug=False):
    if debug: print("enter get_to_ocr_image_pdf_url")
    pattern = r'https?://[\w/\-?=%.]+\.(pdf|png|jpeg|jpg|bmp)'
    if debug: print("try to search")
    match = re.search(pattern,text)
    if match:        
        if debug: print("找到匹配=",match.group())
        return match.group()
    else:
        if debug: print("没有匹配，返回False")
        return False
        

def test_regex(regex, text):
    """测试正则表达式的匹配情况"""
    match = re.search(regex, text)
    if match:
        return match.group()
    else:
        return None


def remove_test(regex, text):
    text = re.sub(regex, "", text)
    return text


def test_regex_all(regex, text):
    """测试正则表达式的匹配情况"""
    matches = re.findall(regex, text)
    if matches:
        return matches
    else:
        return None
            
def remove_time_from_text(text):
    # 匹配时间格式的正则表达式
    time_pattern = r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}:\d{2}|\d{4}-\d{1,2}-\d{1,2}|\d{1,2}:\d{2}:\d{2}|(?=\s)"

    # 使用正则表达式替换时间格式为空字符串
    clean_text = re.sub(time_pattern, "", text).strip().lstrip(".")

    return clean_text





def get_img_size_from_url(url):
    regex=r'_(\d{2,4}_\d{2,4})\.'
    match = re.search(regex,url)
    if match:
        width_height=match.group(1)
        print("match=",width_height)
        arr = width_height.split("_")
        width, height = arr[:2]
        return int(width),int(height)
    return 9999,9999

# u="https://static.dingtalk.com/media/lALPD1za8UFzIqnNAsXNA0A_832_709.png?auth_bizType=IM&bizType=im"
# print(get_img_size_from_url(u))
# import time;time.sleep(333)

# 解码函数
def decode_number(encoded,debug=False):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    try:
        # 将字符转换为对应的数值
        thousands = characters.index(encoded[0])
        sixteens = characters.index(encoded[1])
        units = int(characters.index(encoded[2])/4)
        #print("thousands:",thousands,"sixteens:",sixteens,"units:",units)
        # 根据编码规则重建原始的数字
        number = (thousands * 1024) + (sixteens * 16) + units
        #print("number=",number)
        return number
    except Exception as e:
        print("encoded=",encoded,"decode_number error:",e)
        #raise e

def calc_img_packet(img,debug=False):
    img=img.replace("@","")
    #通过img_packet计算图片url
    def split_and_remove_n(hw):
        # 使用正则表达式找到最后一个"N"并分割，同时保留"N"之前和之后的内容
        parts = re.split(r'(N)(?!.*N)', hw)        
        # 移除列表中的空字符串和第一个"N"
        parts = [part for part in parts if part and part != "N"]
        # 如果需要，重新组合剩余的部分
        result = ''.join(parts)        
        return result
    
    if debug:print("================================\n","enter myfun, img=",img)
    ext = img[:4]
    name = img[4:14]
    hw = img[-7:]
    if debug:print("hw=",hw)
    if "N" not in hw or ".mp3" in img or "pdf" in img:
        print("hw not in",img)
        return
    
    
    #height, width =  [part for part in hw.split("N") if part] 
    height = img[-7:-4]
    width = img[-3:]
    
    if img.startswith("lALP"):
        img_type = ".png"
    elif img[:4] in ["lADP","lQDP"] :
        img_type = ".jpg"
    elif img.startswith("lAPP") or img.startswith("lAHP"):
        img_type = ".bmp"
    elif img.startswith("lQLP"):
        img_type = ".png"
    else:
        img_type = ".png"
        print("强制使用png作为扩展名。img_type not found",img)

    #if debug: print("enter myfun, img=",img,"ext=",ext,"name=",name,"height=",height,"width=",width)
    h = decode_number(height)
    w = decode_number(width)
    url = "https://static.dingtalk.com/media/"
    result = url+ img+ "_" + str(w) + "_" + str(h) +img_type    #+ "?auth_bizType=IM&bizType=im"
    
    if debug: print("result=",result)
    return result



def get_img_url_from_server(img_packet="@lALPM25brIffogLNASPNAl8",debug=True):
    pattern = r'(@[a-zA-Z0-9_-]+)'
    match = re.search(pattern, img_packet)
    if match:
        img_packet =  match.group()
        print("in get_img_url_from_server, format img_packet=",img_packet)

    if img_packet[-4:-3] =="N" and img_packet[-8:-7]=="N":
        print("包含N直接计算")
        return calc_img_packet(img_packet)
    

    conn = http.client.HTTPConnection("127.0.0.1", 12888)
    conn.request("GET", f"/?{img_packet}")
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    print("get imgurl response=",data)
    #{"code":200,"msg":"请求成功","result":{"name":"https:\/\/static.dingtalk.com\/media\/lALPD1Iydp4Z36_867_663.png?auth_bizType=IM&bizType=im"},"timestamp":"1712553472334"}
    # 解析JSON字符串
    if data.startswith('{"code":200,'):
        data_json = json.loads(data)
        # 提取result字段中的name
        url = data_json.get("result", {}).get("name", "")

        return url

def extracet_img_packet(text):
    """
    提取所有符合条件的到数组[{"type":msg_type,"text":text},{"type":msg_type,"text":text2}]
    """
    # 正则表达式匹配
    pattern = r"\[(?:screenshot)?\]\((@[^)]+)\)"
    matches = re.findall(pattern, text)

    img_packets = []  # 初始化图片包列表

    # 检查是否有匹配
    if matches:
        for match in matches:
            # 提取匹配的组
            img_packet = match
            print(f"找到图片包============================================: {img_packet}")
            try:
                url = get_img_url_from_server(img_packet)
                img_packets.append({"type":"img","text":url})  # 将图片包URL添加到列表中
            except Exception as e:
                log(f"=============errmsg============{e}")
    else:
        print("未找到图片包,识别内容类型")
        msg_type, text = identify_content(text)
        img_packets.append({"type":msg_type,"text":text})
    print("result = img_packet",img_packets)
    return img_packets  # 返回图片包列表


def replace_keys_with_values(text, replacement_dict, debug=False):
    """
    Replace keys with corresponding values in the text using the replacement_dict.
    
    Args:
    text (str): The input text to perform replacements on.
    replacement_dict (dict): A dictionary containing the key-value pairs for replacements.
    debug (bool): A flag to enable debug printing. Default is False.
    
    Returns:
    str: The text after performing the replacements.
    """
    

    
    for key, value in replacement_dict.items():       
        if isinstance(key, str) and not key.startswith("text:"):
            if debug:
                matches = re.findall(key, text, re.DOTALL)
                if matches:
                    print("module: lyyre, in replace_keys_with_values, regex_pattern: [", key, "], 匹配的部分：", matches, ", 子文本替换为: ", "<空文本>" or value)
            text = re.sub(key, value, text,flags=re.DOTALL)
        else:
            # For normal strings, use re.escape to ensure special characters are handled correctly
            text = re.sub(re.escape(key), value, text,flags=re.DOTALL)
    
    return text





def extract_links(text):
    pattern = r'https?://\S+'
    links = re.findall(pattern, text)

    return links


def identify_content(text):
    """
    分析并返回类型和提取的网址。

    Args:
        text (_type_): _description_

    Returns:
        类型: img file 或者text
        文本: 提取的网址。如果不是网址，则返回全部文本。
    """
    # 匹配图片的正则表达式模式
    img_pattern = r"https://gchat\.qpic.+|http.+?\.(?:png|jpg|gif|bmp|jpeg)"

    # 匹配文件的正则表达式模式
    file_pattern = r"http.+?\.(?:doc|pdf|docx)"

    # 判断是否为图片
    img_match = re.search(img_pattern, text)
    if img_match:
        return "img", img_match.group()

    # 判断是否为文件
    file_match = re.search(file_pattern, text)
    if file_match:
        return "file", file_match.group()

    # 若不匹配图片或文件的模式，返回其他内容
    return "text", text


def 提取网址(full_text, debug=False):
    pattern = re.compile(r'http[s]?://[\w-]+(?:\.[\w-]+)+[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]')

    #pattern = re.compile(r'http://[^s]*\.pdf')
    result = re.findall(pattern, full_text)
    url = result[0]

    # 去除前后的标点符号
    url = url.strip('\'"<>')
    if debug: print("提取网址结果=" + result[0])
    return result[0]


if __name__ == '__main__':
    t = '"http://43.132.151.196:9993/down.php/f846e67d6ef725ec2a087405abde6b62.pdf"'

    print(提取网址(t))
