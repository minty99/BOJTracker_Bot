import requests
from irc import *
import time
from twitter import *
from bs4 import BeautifulSoup

def get_AC_List(username):
    resp = requests.get('https://www.acmicpc.net/user/' + username)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    all_prob = soup.select("div.col-md-9 > div > div.panel-body")
    prob_ac = all_prob[0].select("span.problem_number > a")
    ret = []
    for t in prob_ac:
        ret += [ int(t.text) ]
    return ret

def get_Update(username):
    print("get_Update: Database for " + username)
    now = get_AC_List(username)
    for p in now:
        if p not in current[username]:
            irc.send(channel[username], "\x02\x03" + "03" + "Accepted: https://boj.kr/" + str(p))
            if username == "mhkim4886": twitter.tweet("Accepted! https://boj.kr/" + str(p))
    current[username] = now[:]

server = "moe.uriirc.org"
port = 16664
nickname = "minty_BOJbot"
channel = { "mhkim4886" : "#minty99", "kipa00" : "#kipa00", "zxcvber" : "#zxcvber", "cmchoi9901" : "#Ryul_99" }
current = { "mhkim4886" : get_AC_List("mhkim4886"), "kipa00" : get_AC_List("kipa00"), "zxcvber": get_AC_List("zxcvber"), "cmchoi9901" : get_AC_List("cmchoi9901") }

users = [ "mhkim4886", "kipa00", "zxcvber", "cmchoi9901" ]

irc = IRC()
irc.connect(server, "#minty99", port, nickname)
irc.join("#kipa00")
irc.join("#zxcvber")
irc.join("#Ryul_99")

twitter = Twitter()

while True:
    for username in users:
        try:
            for i in range(4):
                text = irc.get_text()
                time.sleep(1)
            get_Update(username)
        except Exception as ex: pass
