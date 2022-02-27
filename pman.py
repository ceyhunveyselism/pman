import base64
import datetime
import sys
from re import match
import random
from termcolor import colored
import os
import itertools
import string
import requests
currentVersion = "1.0"



os.system('color')

def err(t, ex):
    print(f"[pman] {colored(f'-err- {ex}', 'red', attrs=['bold'])} {t}")

def info(t):
    print(f"[pman] {colored('-info-', 'grey', attrs=['bold'])} {t}")

def warn(t):
    print(f"[pman] {colored('-warn-', 'yellow', attrs=['bold'])} {t}")

def guess_password(real, printout):
    start = datetime.datetime.now()
    chars = string.ascii_lowercase + string.digits
    attempts = 0
    for password_length in range(1, 9):
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1
            guess = ''.join(guess)
            if guess == real:
                end = datetime.datetime.now()
                info(f"password found: {guess} in {attempts} attempts [{end - start}]")
                return
            # uncomment to display attempts, though will be slower
            if printout:
                info(f"Guess #{attempts}: {guess}")

try:
    sys.argv[1]
except IndexError:
    err("no arguments specified", "0x01")
    exit()

try:
    if sys.argv[1] == "create":
        base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_?-"
        password = ""
        i = 0
        for chr in base:
            i += 1
            password = password + base[random.randrange(1, len(base))]
            if(i == int(sys.argv[2])):
                break
        if(int(sys.argv[2]) > 65):
            warn("you have putted a longer length than 65: the max is 65 due to randrange.")
        info(f"generated: {password}")

        if 3 < len(sys.argv) and 4 < len(sys.argv):
            if sys.argv[3] == "--save":
                f = open(str(sys.argv[4]), "w")
                if 5 < len(sys.argv):
                    if sys.argv[5] == "--encrypt":
                        f.write(base64.b64encode((password).encode("ascii")).decode())
                        info("saved encrypted (b64) password to " + sys.argv[4])
                    else:
                        info("saved password to " + sys.argv[4])
                        f.write(password)
                else:
                    info("saved password to " + sys.argv[4])
                    f.write(password)


    elif sys.argv[1] == "bruteforce":
        warn("bruteforce is only wip and only supports lowercase passwords - sorry!")
        info("forcing...")
        if 3 < len(sys.argv):
            if sys.argv[3] == "--out":
                guess_password(sys.argv[2], True)
        else:
            guess_password(sys.argv[2], False)

    elif sys.argv[1] == "encrypt":
        warn("encrypt is automatically designated to use b64.")
        info("encrypted in base64: " + (base64.b64encode((sys.argv[2]).encode("ascii"))).decode())

    elif sys.argv[1] == "decrypt":
        warn("decrypt is automatically designated to use b64.")
        info("decrypted in base64: " + (base64.b64decode((sys.argv[2]).encode("ascii"))).decode())

    elif sys.argv[1] == "download":
        if(not sys.argv[2].startswith("https://")):
            r = requests.get("https://" + sys.argv[2], allow_redirects=True)
        else:
            r = requests.get(sys.argv[2], allow_redirects=True)
        open(str(sys.argv[3]), "wb").write(r.content)
        info("file successfully downloaded to " + sys.argv[3])

    else:
        err("command not recognized", "0x04")

except ValueError:
    err(f"wrong type provided", "0x03")

except IndexError:
    err(f"not enough arguments for command '{sys.argv[1]}'", "0x02")

except KeyboardInterrupt:
    exit(0)
