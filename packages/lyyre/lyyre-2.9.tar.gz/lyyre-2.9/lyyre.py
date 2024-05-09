import re

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
                print(f"=============errmsg============{e}")
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
