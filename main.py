#ПРИМЕР ССЫЛКИ: url = 'https://hkar.ru/15s32'
from bs4 import BeautifulSoup
from itertools import product
from random import *
import os, threading, queue, requests
from colorama import init
init()
from colorama import Fore, Back, Style


print(Back.RED + 'ЧТОБЫ ПОМЕНЯТЬ КОЛИЧЕСТВО ПОТОКОВ ИЗМЕНИТЕ ФАЙЛ DATA.TXT')
print(Back.RED + 'ПЕРЕД ИЗМЕНЕНИЕМ ПРОЧИТАЙТЕ README.TXT, ИНАЧЕ ВСЕ СЛОМАЕТСЯ' + Style.RESET_ALL)

with open('data.txt') as dat:
    first_nums = dat.readline().split()
    thr = int(dat.readline())

def download(url, name):
    if os.path.isdir('pics/'):
        with open('pics/' + name, 'wb') as f:
            f.write(requests.get(url).content)
    else:
        os.mkdir('pics')
        with open('pics/' + name, 'wb') as f:
            f.write(requests.get(url).content)
        
data = queue.Queue()
random_url = list(product('qwertyuiopasdfghjklzxcvbnm0123456789', repeat = 3))
shuffle(random_url)

for i in random_url:
    data.put(i)


def main(data):
    while not data.empty():
        task = data.get()
        combin = choice(first_nums) + ''.join(task)
        url = 'https://hkar.ru/' + combin
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        images = soup.findAll('img', itemprop='url')
        if len(images) != 0:
            image_url = str(images[0]).replace('"',' ').split()[4]
            download(image_url, ''.join(combin) + '.jpg')
            prnt = url + '  succeed'
            print(Fore.GREEN + prnt)
        else:
            prnt = url + "  hasn't image"
            print(Fore.YELLOW + prnt)
        data.task_done()


for i in range(thr):
    thread = threading.Thread(target=main, args=(data, ))
    thread.start()
    
    


