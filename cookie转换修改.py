def hex_to_text(hex_string):
    """
    将十六进制字符串转换为文本
    """
    try:
        text = bytes.fromhex(hex_string).decode('utf-8')
        return text
    except ValueError:
        return None

def text_to_hex(text):
    """
    将文本转换为十六进制字符串
    """
    hex_string = text.encode('utf-8').hex()
    return hex_string

def main():
    hex_input = input("请输入十六进制字符串：")
    text_result = hex_to_text(hex_input)

    if text_result:
        print("转换结果为：", text_result)
        modify = input("是否需要修改字段内容？(y/n): ")

        if modify.lower() == 'y':
            new_text = input("请输入新的字段内容：")
            new_hex = text_to_hex(new_text)
            print("新的十六进制字符串为：", new_hex)
        else:
            print("程序结束。")

    else:
        print("输入的不是有效的十六进制字符串。")

if __name__ == "__main__":
    main()
