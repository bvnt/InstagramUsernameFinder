import queue
import threading
import requests

#https://github.com/izzeterdogan
#https://twitter.com/izterdogn

def check(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.268",
        "Accept": "*/*",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "X-IG-WWW-Claim": "0",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.instagram.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    r = requests.get(url=url, headers=headers)
    status = r.status_code
    if status == 404:
        print(f"Username Found: {username}")
    elif status == 200:
        #pass #Başarısız sonuçların çıktısını almak istemiyorsanız; Bu satırı etkin ve sonraki satırı devre dışı bırakın. #If you do not want to print out the failed results; Make this line active and the following line inactive.
        print(f"Failed: {username}")
    else:
        print("There is a problem, ustaa...")
def worker():
    while True:
        username = q.get()
        if username is None:
            break
        check(username)
        q.task_done()
file_path = 'usernames.txt'
usernames = []
with open(file_path, 'r',encoding="utf-8") as file:
    usernames = [line.strip() for line in file]
q = queue.Queue()
for username in usernames:
    q.put(username)
num_worker_threads = 5 #Thread sayısını değişebilirsiniz. #You can change the number of threads.
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
q.join()
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()