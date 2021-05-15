#Cyberdrop Gallery Downloader Originally by nixxin
#Made better(?) by Jules--Winnfield

import requests
import os
import re
import json #test
import pathlib
from colorama import Fore, Style
from geturls import Extrair_Links
from multiprocessing import Pool
import multiprocessing
import traceback


def log(text, style):
    print(style + str(text) + Style.RESET_ALL)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def download(passed_from_main):
    _path = passed_from_main[0]
    _item = passed_from_main[1]
    j = 1
    try:
        while True:
            try:
                filename = _item[_item.rfind("/") + 1:]
                _url = _item

                if filename == "cyberdrop.me-downloaders":

                    break

                if os.path.isfile(_path + str(filename)):
                    log("           " + filename + " already exists.", Fore.LIGHTBLACK_EX)
                    break

                log("        Downloading " + filename + "...", Fore.LIGHTBLACK_EX)

                response = requests.get(_url, stream=True)
                with open(_path+str(filename), "wb") as out_file:
                    for chunk in response.iter_content(chunk_size=None):
                        if chunk:
                            out_file.write(chunk)
                del response
                if out_file:
                    break
            except Exception as e:
                track = traceback.format_exc()
                log(track, Fore.RED)
                os.remove(_path + str(filename))
                log("Failed attempt " + str(j) + " for " + filename + "\n", Fore.RED)
                log("Retrying "+ filename + "...", Fore.YELLOW)
                j += 1

    except Exception as e:
        print(e)
        print("Failed to Download")

if __name__ == '__main__':
    log("", Fore.RESET)

    headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    total = 0
    paths = pathlib.Path(__file__).parent.absolute()

    clear()

    if os.path.isfile("URLs.txt"):
        print("URLs.txt exists")
    else:
        f = open("URLs.txt", "w+")
        print("URLs.txt created")

    if os.stat("URLs.txt").st_size == 0:
        print("Please put URLs in URLs.txt")

    file_object = open("URLs.txt", "r")
    for line in file_object:
        url = line.rstrip()

        n = requests.get(url, headers=headers)
        a1 = n.text
        di = a1[a1.find("<title>") + 7 : a1.find("</title>")]
        di = di.split("–")[0]
        di = di[7:-1]
        di = re.findall('^[^\[]*', di)
        di = di[0].rstrip()
        di += "/"

        links = []

        print("\n======================================================\n")

        print("\nCollecting file links from " + url + "...")
        links = Extrair_Links(url)

        if links is None:
            print()
            input(url + " Couldn't find pictures.")
            exit()
        else:
            for item in links:
                total += 1

        path = str(paths) + "/" + di
        print()
        print("       URL       " + url)
        print("       DIR       " + di)
        print()
        try:
            os.mkdir(path)
        except OSError:
            log("Creation of directory %s failed" % path, Fore.YELLOW)
        else:
            print()
            print ("Directory %s was created" % path)
        print()

        total = int(total)
        i = 0
        pass_to_func = []
        for link in links:
            pass_to_func.append([path, link])
            i += 1

        print("Downloading " + str(len(pass_to_func)) + " files...")
        pool = Pool(processes = multiprocessing.cpu_count())
        proc = pool.map_async(download, pass_to_func)
        proc.wait()
        pool.close()
                
    ex = input("\nFinished. Press enter to quit.")
