import re

def parse_hm(text: str):
    """
    解析字符串中的小时(h)和分钟(m)数字
    支持格式："1h 31m", "*5h*", "*8m*", "2h", "30m"
    :param text: 待解析字符串
    :return: (hour, minute)，无对应数字返回 None
    """
    # 查找h前面的数字
    h_match = re.search(r'(\d+)h', text)
    # 查找m前面的数字
    m_match = re.search(r'(\d+)m', text)

    hour = int(h_match.group(1)) if h_match else 0
    minute = int(m_match.group(1)) if m_match else 0
    len    =  60*hour + minute
    return len


# 测试用例
if __name__ == "__main__":
    cases = [
        "1h 31m",
        "*5h*",
        "*8m*",
        "2h",
        "30m",
        "*10h*45m",
        "no hm here"
    ]
    for case in cases:
        t = parse_hm(case)
        print(f"{t}m")
