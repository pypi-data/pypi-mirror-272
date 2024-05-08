import hashlib
import base64
from typing import Any
import pyperclip
import emoji
from cryptography.fernet import Fernet
from tqdm import tqdm


def md5_encrypt(input_string: str, salt: Any = None):
    """
    对输入字符串进行md5加密

    :param input_string: 输入字符串
    :param salt: 盐值，可以不填
    """
    use_salt_bool = False

    if salt is not None:
        try:
            salt = str(salt)
        except Exception as e:
            raise Exception(f"salt转化为字符串失败, {e}")
        use_salt_bool = True

    md5 = hashlib.md5()
    if use_salt_bool:
        salt = salt.encode('utf-8')
        md5.update(input_string.encode('utf-8') + salt)
    else:
        md5.update(input_string.encode('utf-8'))
    return md5.hexdigest()

def base64_encode(input_string: str):
    """
    对输入字符串进行base64编码

    :param input_string: 输入字符串
    """
    # 将字符串编码为字节
    input_bytes = input_string.encode('utf-8')
    # 对字节进行 Base64 编码
    encoded_bytes = base64.b64encode(input_bytes)
    # 将编码后的字节转换为字符串并返回
    return encoded_bytes.decode('utf-8')

def base64_decode(encoded_string: str):
    """
    对输入字符串进行base64解码

    :param encoded_string: 输入字符串
    """
    # 将字符串转换为字节
    encoded_bytes = encoded_string.encode('utf-8')
    # 对字节进行 Base64 解码
    decoded_bytes = base64.b64decode(encoded_bytes)
    # 将解码后的字节转换为字符串并返回
    return decoded_bytes.decode('utf-8')

def copy_to_clipboard(data: str) -> None:
    """
    将数据复制到剪贴板。

    Parameters:
        data (str): 要复制到剪贴板的数据。

    Returns:
        None
    """
    # 判断data是否为字符串
    if not isinstance(data, str):
        raise ValueError("Data must be a string.")

    # 使用pyperclip库将数据复制到剪贴板
    pyperclip.copy(data)

def _validate_message_type(func):
    def wrapper(message):
        if not isinstance(message, str):
            print(message)  # 如果message不是字符串类型，则直接输出message
            return None  # 返回None，不执行被装饰的函数
        else:
            return func(message)  # 如果message是字符串类型，则执行被装饰的函数
    return wrapper

@_validate_message_type
def success_toast(message: str):
    """
    输出成功消息，并添加成功的表情符号
    """
    success_emoji = emoji.emojize(':thumbs_up:' * 3, language='alias')
    print(f"{success_emoji} Success: {message}")

@_validate_message_type
def warning_toast(message: str):
    """
    输出警告消息，并添加警告的表情符号
    """
    warning_emoji = emoji.emojize(':warning:' * 3, language='alias')
    print(f"{warning_emoji} Warning: {message}")

@_validate_message_type
def failure_toast(message: str):
    """
    输出失败消息，并添加失败的表情符号
    """
    failure_emoji = emoji.emojize(':thumbs_down:' * 3, language='alias')
    print(f"{failure_emoji} Failure: {message}")


def fernet_generate_key():
    """
    生成一个随机的Fernet密钥
    """
    return Fernet.generate_key().decode('utf-8')

def fernet_jiami(input_string: str, key: str):
    """
    使用Fernet库对输入的字符串进行加密
    :param input_string: 要加密的字符串
    :param key: Fernet密钥
    """
    # 检查Fernet密钥是否符合格式
    try:
        key = str(key).encode('utf-8')
        # 创建 Fernet 对象
        cipher_suite = Fernet(key)
    except Exception as e:
        mes = f"Fernet密钥格式错误: {e},请使用Fernet.generate_key()生成密钥"
        raise Exception(mes)

    # 将字符串转换为字节型
    input_bytes = input_string.encode('utf-8')
    # 加密字符串
    encrypted_text = cipher_suite.encrypt(input_bytes).decode('utf-8')

    return encrypted_text

def fernet_jiemi(input_string: str, key: str):
    """
    使用Fernet库对输入的字符串进行解密
    :param input_string: 要解密的字符串
    :param key: Fernet密钥
    """

    # 检查Fernet密钥是否符合格式
    try:
        key = str(key).encode('utf-8')
        # 创建 Fernet 对象
        cipher_suite = Fernet(key)
    except Exception as e:
        mes = f"Fernet密钥格式错误: {e}"
        raise Exception(mes)

    # 将字符串转换为字节型
    input_bytes = input_string.encode('utf-8')

    # 解密字符串
    decrypted_text = cipher_suite.decrypt(input_bytes).decode('utf-8')

    return decrypted_text

def process_with_progress(iterable, process_func, desc="处理中...") -> list:
    """
    使用 tqdm 封装的通用函数，用于在处理过程中显示进度条。
    对iterable每一项进行process_func处理，并返回处理后的结果列表。
    Parameters:
        iterable (iterable): 要处理的可迭代对象。
        process_func (callable): 处理每个元素的函数。
        desc (str, optional): 进度条的描述信息，默认为 "处理中..."。

    Returns:
        list: 处理后的结果列表。

    # 使用参考
    def square(x):
        import time
        time.sleep(0.1)
        return x * x

    # 使用 process_with_progress 函数处理一个列表，对每个元素求平方，并显示进度条
    input_list = [ n for n in range(1, 100) ]
    processed_results = process_with_progress(input_list, square)
    print(processed_results)
    """
    results = []
    with tqdm(iterable, desc=desc, unit="item") as pbar:
        for item in pbar:
            result = process_func(item)
            results.append(result)
    return results

# 测试函数
if __name__ == "__main__":
    # 测试成功消息
    success_toast("Task completed successfully!")

    # 测试警告消息
    warning_toast("Low disk space detected.")

    # 测试失败消息
    failure_toast("Error: Connection timed out.")

    # 测试非字符串消息
    failure_toast(123)  # 直接输出数字 123，不执行函数from cryptography.fernet import Fernet

    # key = Fernet.generate_key().decode('utf-8')
    # print(key)
    s = 'hello world'
    print(fernet_jiami(s, '5nMwLbESgNf5Jb3E36cjzUY50Sa11bCA37yBguyMLHA='))
    print(fernet_jiemi('gAAAAABmIgozSAnuGcLWDl-nCqPqpUSAvX3CN4gziLlJZAZ8GJ3kihQw6VSjBfAIqj3NdjNHjUk8JlO8ylDzPtbGKf8q002HZQ==', '5nMwLbESgNf5Jb3E36cjzUY50Sa11bCA37yBguyMLHA='))
