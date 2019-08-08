import datetime
import os
import constants
import subprocess


def get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:")
    return now


def explore_host(hostname):
    p = 'explorer "\\\\' + hostname + '\C$"'
    subprocess.Popen(p)


def ping_computer(hostname):
    os.system("start cmd /c ping " + hostname +" -t")


def test_connection(hostname):
    c = os.system("ping -n 1 " + hostname)
    if c == 0:
        connected = True
    else:
        connected = False
    return connected


def generate_password():

    def get_letter_month(val):
        switcher = {
            1: "St",
            2: "Lu",
            3: "Ma",
            4: "Kw",
            5: "Ma",
            6: "Cz",
            7: "Li",
            8: "Si",
            9: "Wr",
            10: "Pa",
            11: "Li",
            12: "Gr"
        }
        return switcher.get(val, "")

    def get_letter_weekday(val):
        switcher = {
            0: "Po",
            1: "Wt",
            2: "Śr",
            3: "Cz",
            4: "Pi",
            5: "So",
            6: "Ni"
        }
        return switcher.get(val, "")

    now = datetime.datetime.today()
    password = constants.PASS_PREFIX + get_letter_month(now.month) + get_letter_weekday(now.weekday()) + str(now.hour)
    return password
